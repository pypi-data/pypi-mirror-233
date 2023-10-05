use std::{
    any::Any,
    sync::{Arc, Mutex},
};

use egglog::sort::{FromSort, IntoSort, StringSort};
use egglog::{
    ast::{Expr, Literal, Symbol},
    sort::{I64Sort, Sort},
    util::IndexMap,
    ArcSort, EGraph, PrimitiveLike, TypeInfo, Value,
};
use pyo3::{types::PyDict, AsPyPointer, IntoPy, PyObject, Python};

#[derive(Debug, PartialEq, Eq, Hash, Clone, Copy)]
pub enum PyObjectIdent {
    // Unhashable objects use the object ID as the key
    Unhashable(usize),
    // Hashable objects use the hash of the type as well as the hash of the object as the key
    // (need type hash as well, b/c different objects can have the same hash https://docs.python.org/3/library/functions.html#hash)
    Hashable(isize, isize),
}

#[derive(Debug)]
pub struct PyObjectSort {
    name: Symbol,
    // Use an index map so that we can point to a value with an index we can store in the value
    pub objects: Mutex<IndexMap<PyObjectIdent, PyObject>>,
}

impl PyObjectSort {
    pub fn new(name: Symbol) -> Self {
        Self {
            name,
            objects: Default::default(),
        }
    }

    pub fn load(&self, value: &Value) -> (PyObjectIdent, PyObject) {
        let objects = self.objects.lock().unwrap();
        let i = value.bits as usize;
        let (ident, obj) = objects.get_index(i).unwrap();
        (*ident, obj.clone())
    }
    pub fn store(&self, obj: PyObject) -> Value {
        // Try hashing the object, if it fails, then it's unhashable, and store with ID
        let ident = Python::with_gil(|py| {
            let o = obj.as_ref(py);
            match o.hash() {
                Ok(hash) => PyObjectIdent::Hashable(o.get_type().hash().unwrap(), hash),
                Err(_) => PyObjectIdent::Unhashable(obj.as_ptr() as usize),
            }
        });
        let mut objects = self.objects.lock().unwrap();
        let (i, _) = objects.insert_full(ident, obj);
        Value {
            tag: self.name,
            bits: i as u64,
        }
    }

    fn get_value(&self, key: &PyObjectIdent) -> Value {
        let objects = self.objects.lock().unwrap();
        let i = objects.get_index_of(key).unwrap();
        Value {
            tag: self.name,
            bits: i as u64,
        }
    }
}

impl Sort for PyObjectSort {
    fn name(&self) -> Symbol {
        self.name
    }

    fn as_arc_any(self: Arc<Self>) -> Arc<dyn Any + Send + Sync + 'static> {
        self
    }

    #[rustfmt::skip]
    fn register_primitives(self: Arc<Self>, typeinfo: &mut TypeInfo) {
        typeinfo.add_primitive(Ctor {
            name: "py-object".into(),
            py_object: self.clone(),
            i64:typeinfo.get_sort(),
        });
        typeinfo.add_primitive(Eval {
            name: "py-eval".into(),
            py_object: self.clone(),
            string: typeinfo.get_sort(),
        });
        typeinfo.add_primitive(Exec {
            name: "py-exec".into(),
            py_object: self.clone(),
            string: typeinfo.get_sort(),
        });
        typeinfo.add_primitive(Dict {
            name: "py-dict".into(),
            py_object: self.clone(),
        });
        typeinfo.add_primitive(DictUpdate {
            name: "py-dict-update".into(),
            py_object: self.clone(),
        });
        typeinfo.add_primitive(ToString {
            name: "py-to-string".into(),
            py_object: self.clone(),
            string: typeinfo.get_sort(),
        });
        typeinfo.add_primitive(FromString {
            name: "py-from-string".into(),
            py_object: self.clone(),
            string: typeinfo.get_sort(),
        });
        typeinfo.add_primitive(FromInt {
            name: "py-from-int".into(),
            py_object: self,
            int: typeinfo.get_sort(),
        });
    }
    fn make_expr(&self, _egraph: &EGraph, value: Value) -> (usize, Expr) {
        assert!(value.tag == self.name());
        let (ident, _) = self.load(&value);
        let children = match ident {
            PyObjectIdent::Unhashable(id) => {
                vec![Expr::Lit(Literal::Int(id as i64))]
            }
            PyObjectIdent::Hashable(type_hash, hash) => {
                vec![
                    Expr::Lit(Literal::Int(type_hash as i64)),
                    Expr::Lit(Literal::Int(hash as i64)),
                ]
            }
        };
        (1, Expr::call("py-object", children))
    }
}

struct Ctor {
    name: Symbol,
    py_object: Arc<PyObjectSort>,
    i64: Arc<I64Sort>,
}

impl PrimitiveLike for Ctor {
    fn name(&self) -> Symbol {
        self.name
    }

    fn accept(&self, types: &[ArcSort]) -> Option<ArcSort> {
        match types {
            [id] if id.name() == self.i64.name() => Some(self.py_object.clone()),
            [type_hash, hash]
                if type_hash.name() == self.i64.name() && hash.name() == self.i64.name() =>
            {
                Some(self.py_object.clone())
            }
            _ => None,
        }
    }

    fn apply(&self, values: &[Value]) -> Option<Value> {
        let ident = match values {
            [id] => PyObjectIdent::Unhashable(i64::load(self.i64.as_ref(), id) as usize),
            [type_hash, hash] => PyObjectIdent::Hashable(
                i64::load(self.i64.as_ref(), type_hash) as isize,
                i64::load(self.i64.as_ref(), hash) as isize,
            ),
            _ => unreachable!(),
        };
        self.py_object.get_value(&ident).into()
    }
}

/// Supports calling (py-eval <str-obj> <globals-obj> <locals-obj>)
struct Eval {
    name: Symbol,
    py_object: Arc<PyObjectSort>,
    string: Arc<StringSort>,
}

impl PrimitiveLike for Eval {
    fn name(&self) -> Symbol {
        self.name
    }

    fn accept(&self, types: &[ArcSort]) -> Option<ArcSort> {
        match types {
            [str, locals, globals]
                if str.name() == self.string.name()
                    && locals.name() == self.py_object.name()
                    && globals.name() == self.py_object.name() =>
            {
                Some(self.py_object.clone())
            }
            _ => None,
        }
    }

    fn apply(&self, values: &[Value]) -> Option<Value> {
        let code: Symbol = Symbol::load(self.string.as_ref(), &values[0]);
        let res_obj: PyObject = Python::with_gil(|py| {
            let (_, globals) = self.py_object.load(&values[1]);
            let globals = Some(globals.downcast::<PyDict>(py).unwrap());
            let (_, locals) = self.py_object.load(&values[2]);
            let locals = Some(locals.downcast::<PyDict>(py).unwrap());
            py.eval(code.into(), globals, locals).unwrap().into()
        });
        Some(self.py_object.store(res_obj))
    }
}

/// Copies the locals, execs the Python string, then returns the copied version of the locals with any updates
/// (py-exec <str-obj> <globals-obj> <locals-obj>)
struct Exec {
    name: Symbol,
    py_object: Arc<PyObjectSort>,
    string: Arc<StringSort>,
}

impl PrimitiveLike for Exec {
    fn name(&self) -> Symbol {
        self.name
    }

    fn accept(&self, types: &[ArcSort]) -> Option<ArcSort> {
        match types {
            [str, locals, globals]
                if str.name() == self.string.name()
                    && locals.name() == self.py_object.name()
                    && globals.name() == self.py_object.name() =>
            {
                Some(self.py_object.clone())
            }
            _ => None,
        }
    }

    fn apply(&self, values: &[Value]) -> Option<Value> {
        let code: Symbol = Symbol::load(self.string.as_ref(), &values[0]);
        let locals: PyObject = Python::with_gil(|py| {
            let (_, globals) = self.py_object.load(&values[1]);
            let globals = globals.downcast::<PyDict>(py).unwrap();
            let (_, locals) = self.py_object.load(&values[2]);
            let locals = locals.downcast::<PyDict>(py).unwrap().copy().unwrap();
            py.run(code.into(), Some(globals), Some(locals)).unwrap();
            locals.into()
        });
        Some(self.py_object.store(locals))
    }
}

/// (py-dict [<key-object> <value-object>]*)
struct Dict {
    name: Symbol,
    py_object: Arc<PyObjectSort>,
}

impl PrimitiveLike for Dict {
    fn name(&self) -> Symbol {
        self.name
    }

    fn accept(&self, types: &[ArcSort]) -> Option<ArcSort> {
        // Should have an even number of args
        if types.len() % 2 != 0 {
            return None;
        }
        for tp in types.iter() {
            // All tps should be object
            if tp.name() != self.py_object.name() {
                return None;
            }
        }
        Some(self.py_object.clone())
    }

    fn apply(&self, values: &[Value]) -> Option<Value> {
        let dict: PyObject = Python::with_gil(|py| {
            let dict = PyDict::new(py);
            // Update the dict with the key-value pairs
            for i in values.chunks_exact(2) {
                let key = self.py_object.load(&i[0]).1;
                let value = self.py_object.load(&i[1]).1;
                dict.set_item(key, value).unwrap();
            }
            dict.into()
        });
        Some(self.py_object.store(dict))
    }
}

/// Supports calling (py-dict-update <dict-obj> [<key-object> <value-obj>]*)
struct DictUpdate {
    name: Symbol,
    py_object: Arc<PyObjectSort>,
}

impl PrimitiveLike for DictUpdate {
    fn name(&self) -> Symbol {
        self.name
    }

    fn accept(&self, types: &[ArcSort]) -> Option<ArcSort> {
        // Should have an odd number of args, with all the pairs plus the first arg
        if types.len() % 2 == 0 {
            return None;
        }
        for (i, tp) in types.iter().enumerate() {
            // First tp should be dict
            if i == 0 {
                if tp.name() != self.py_object.name() {
                    return None;
                }
            }
            // All other tps should be object
            else if tp.name() != self.py_object.name() {
                return None;
            }
        }
        Some(self.py_object.clone())
    }

    fn apply(&self, values: &[Value]) -> Option<Value> {
        let dict: PyObject = Python::with_gil(|py| {
            // Copy the dict so we can mutate it and return it
            let (_, dict) = self.py_object.load(&values[0]);
            let dict = dict.downcast::<PyDict>(py).unwrap().copy().unwrap();
            // Update the dict with the key-value pairs
            for i in values[1..].chunks_exact(2) {
                let key = self.py_object.load(&i[0]).1;
                let value = self.py_object.load(&i[1]).1;
                dict.set_item(key, value).unwrap();
            }
            dict.into()
        });
        Some(self.py_object.store(dict))
    }
}

/// (py-to-string <obj>)
struct ToString {
    name: Symbol,
    py_object: Arc<PyObjectSort>,
    string: Arc<StringSort>,
}

impl PrimitiveLike for ToString {
    fn name(&self) -> Symbol {
        self.name
    }

    fn accept(&self, types: &[ArcSort]) -> Option<ArcSort> {
        match types {
            [obj] if obj.name() == self.py_object.name() => Some(self.string.clone()),
            _ => None,
        }
    }

    fn apply(&self, values: &[Value]) -> Option<Value> {
        let obj: String = Python::with_gil(|py| {
            let (_, obj) = self.py_object.load(&values[0]);
            obj.extract(py).unwrap()
        });
        let symbol: Symbol = obj.into();
        symbol.store(self.string.as_ref())
    }
}

/// (py-from-string <str>)
struct FromString {
    name: Symbol,
    py_object: Arc<PyObjectSort>,
    string: Arc<StringSort>,
}

impl PrimitiveLike for FromString {
    fn name(&self) -> Symbol {
        self.name
    }

    fn accept(&self, types: &[ArcSort]) -> Option<ArcSort> {
        match types {
            [str] if str.name() == self.string.name() => Some(self.py_object.clone()),
            _ => None,
        }
    }

    fn apply(&self, values: &[Value]) -> Option<Value> {
        let str = Symbol::load(self.string.as_ref(), &values[0]).to_string();
        let obj: PyObject = Python::with_gil(|py| str.into_py(py));
        Some(self.py_object.store(obj))
    }
}

// (py-from-int <int>)
struct FromInt {
    name: Symbol,
    py_object: Arc<PyObjectSort>,
    int: Arc<I64Sort>,
}

impl PrimitiveLike for FromInt {
    fn name(&self) -> Symbol {
        self.name
    }

    fn accept(&self, types: &[ArcSort]) -> Option<ArcSort> {
        match types {
            [int] if int.name() == self.int.name() => Some(self.py_object.clone()),
            _ => None,
        }
    }

    fn apply(&self, values: &[Value]) -> Option<Value> {
        let int = i64::load(self.int.as_ref(), &values[0]);
        let obj: PyObject = Python::with_gil(|py| int.into_py(py));
        Some(self.py_object.store(obj))
    }
}
