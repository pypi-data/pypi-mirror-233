
from typing import List
import zsp_dataclasses.impl.context as ctxt_api
import vsc_dataclasses.impl.context as vsc_ctxt
import vsc_dataclasses.impl.pyctxt as vsc_pyctxt

from .data_type_action import DataTypeAction
from .data_type_component import DataTypeComponent
from .data_type_activity_replicate import DataTypeActivityReplicate
from .data_type_activity_sequence import DataTypeActivitySequence
from .data_type_activity_traverse import DataTypeActivityTraverse
from .data_type_function import DataTypeFunction
from .data_type_function_import import DataTypeFunctionImport
from .data_type_function_param_decl import DataTypeFunctionParamDecl
from .type_exec import TypeExec
from .type_expr_method_call_static import TypeExprMethodCallStatic
from .type_field_activity import TypeFieldActivity
from .type_proc_stmt_var_decl import TypeProcStmtVarDecl
from .type_proc_stmt_expr import TypeProcStmtExpr
from .type_proc_stmt_scope import TypeProcStmtScope


class Context(vsc_pyctxt.Context,ctxt_api.Context):

    def __init__(self):
        super().__init__()
        self._action_t_m = {}
        self._comp_t_m = {}
        self._data_t_func_m = {}
        self._data_t_func_l = []

    def findDataTypeAction(self, name) -> 'DataTypeAction':
        if name in self._action_t_m.keys():
            return self._action_t_m[name]
        else:
            return None
    
    def mkDataTypeAction(self, name) -> DataTypeAction:
        return DataTypeAction(self, name)

    def addDataTypeAction(self, t : DataTypeAction) -> bool:
        if t._name not in self._action_t_m.keys():
            self._action_t_m[t._name] = t
            return True
        else:
            return False

    def findDataTypeComponent(self, name) -> 'DataTypeComponent':
        if name in self._comp_t_m.keys():
            return self._comp_t_m[name]
        else:
            return None

    def mkDataTypeComponent(self, name) -> 'DataTypeComponent':
        return DataTypeComponent(name)

    def addDataTypeComponent(self, t : 'DataTypeComponent') -> bool:
        if t._name not in self._comp_t_m.keys():
            self._comp_t_m[t._name] = t
            return True
        else:
            return False

    def mkDataTypeActivityReplicate(self, count) -> 'DataTypeActivityReplicate':
        return DataTypeActivityReplicate(count)

    def mkDataTypeActivitySequence(self) -> 'DataTypeActivitySequence':
        return DataTypeActivitySequence()

    def mkDataTypeActivityTraverse(self, target, with_c):
        return DataTypeActivityTraverse(target, with_c)

    def mkDataTypeFunction(self,
                           name : str,
                           rtype : vsc_ctxt.DataType,
                           own_rtype : bool,
                           is_target : bool,
                           is_solve : bool):
        return DataTypeFunction(name, rtype)
    
    def addDataTypeFunction(self, f):
        if f.name() not in self._data_t_func_m.keys():
            self._data_t_func_m[f.name()] = f
            self._data_t_func_l.append(f)

    def getDataTypeFunctions(self):
        return self._data_t_func_l
    
    def mkDataTypeFunctionImport(self,
                                 lang,
                                 is_target,
                                 is_solve):
        return DataTypeFunctionImport(lang, is_target, is_solve)

    def mkDataTypeFunctionParamDecl(self,
                                name,
                                dir : ctxt_api.ParamDir,
                                type : vsc_ctxt.DataType,
                                own : bool,
                                init : vsc_ctxt.TypeExpr) -> ctxt_api.DataTypeFunctionParamDecl:
        return DataTypeFunctionParamDecl(name, dir, type, own, init)
    
    def mkTypeExec(self,
                   kind,
                   body):
        return TypeExec(kind, body)


    def mkTypeFieldActivity(self, name, type : 'DataTypeActivity', owned):
        return TypeFieldActivity(name, type)
    
    def mkTypeFieldPhy(self,
        name,
        dtype : 'DataType',
        own_dtype : bool,
        attr,
        init : 'ModelVal') -> 'TypeFieldPhy':
        print("mkTypeFieldPhy: %s" % name)
        if name.endswith(".Entry"):
            raise Exception("Creating action-named field")
        else:
            return super().mkTypeFieldPhy(name, dtype, own_dtype, attr, init)
    
    def mkTypeFieldRef(self,
        name,
        dtype : 'DataType',
        attr) -> 'TypeFieldRef':
        print("mkTypeFieldRef: %s" % name)
        if name.endswith(".Entry"):
            raise Exception("Creating action-named field")
        else:
            return super().mkTypeFieldRef(name, dtype, attr)
    
    def mkTypeExprMethodCallStatic(self, 
                                   target: DataTypeFunction, 
                                   params: List[vsc_ctxt.TypeExpr]):
        return TypeExprMethodCallStatic(target, params)

    def mkTypeProcStmtExpr(self, expr):
        return TypeProcStmtExpr(expr)

    def mkTypeProcStmtVarDecl(self, name, type, init):
        return TypeProcStmtVarDecl(name, type, init)
    
    def mkTypeProcStmtScope(self):
        return TypeProcStmtScope()

