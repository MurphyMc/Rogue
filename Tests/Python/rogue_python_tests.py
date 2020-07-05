from __future__ import print_function
import unittest
#from pytest import *

def msg (*args):
  #print(*args)
  pass


def _configure ():
  import pytest
  g = globals()
  for k in dir(pytest):
    if k not in g:
      g[k] = getattr(pytest, k)
  global f, b
  f = Foo()
  b = f.new_bar("MyBar")

class TestPythonBasics (unittest.TestCase):
  @classmethod
  def setUpClass (cls):
    _configure()


  def test_rogue_globals (self):
    # Test Rogue globals

    # Global routines are easily publicly accessible
    self.assertEqual(rogue_routine(), 121)

    # Properties are accessible using Global singleton
    self.assertEqual(Global.singleton.rogue_global, 122)


  def test_global_methods (self):
    # Test Global methods

    self.assertEqual(f.gf_square(5), 25)
    self.assertEqual(Foo.gf_square(5), 25)


  def test_rogue_object_properties (self):
    # Test accessing Rogue properties from Python

    self.assertEqual( f.prop_str, "hello" )
    self.assertEqual( f.prop_int, 42 )
    self.assertIs( f.prop_bar, None )

    f.prop_str = "world"
    f.prop_int = 100
    f.prop_bar = b

    self.assertEqual( f.prop_str, "world" )
    self.assertEqual( f.prop_int, 100 )
    self.assertIsInstance(f.prop_bar, Bar)
    self.assertEqual( str(f.prop_bar), "<Bar MyBar>")

    f.prop_bar = Bar("PyBar")

    self.assertEqual(str(f.prop_bar), "<Bar PyBar>")

    f.prop_bar = f.prop_bar

    self.assertEqual(f.f_ss("hello"), "HELLO")


    f.prop_bar = None
    self.assertIs(f.prop_bar, None)

    f.prop_str = None
    self.assertIs(f.prop_str, None)

  def test_rogue_global_properties (self):
    self.assertEqual(f.gprop_int, 2000)
    self.assertEqual(Foo.gprop_int, 2000)
    f.gprop_int = 2001
    self.assertEqual(f.gprop_int, 2001)
    self.assertEqual(Foo.gprop_int, 2001)
    Foo.gprop_int = 2002
    self.assertEqual(f.gprop_int, 2002)
    self.assertEqual(Foo.gprop_int, 2002)


class TestPythonBindingsCalls (unittest.TestCase):
  @classmethod
  def setUpClass (cls):
    _configure()


  def test_rogue_function_objects (self):
    # Test calling Rogue function objects from Python

    func = f.f_sf("cap this")
    #msg(func)
    self.assertEqual(func(), "CAP THIS")


  def test_rogue_calling_python (self):
    # Test calling from Rogue into Python...

    def pyfunc_v_i ():
      r = 99
      msg("Python in pyfunc_v_i, returning " + str(r))
      return r

    def pyfunc_s_i (s):
      r = int(s) * 10
      msg("Python in pyfunc_s_i, returning " + str(r))
      return r

    def pyfunc_s_o (s):
      r = Bar("Py"+s)
      msg("Python in pyfunc_s_o, returning " + str(r))
      return r

    def pyfunc_i_s (i):
      r = "!" * i
      msg("Python in pyfunc_i_s, returning " + str(r))
      return r

    f.prop_f_v_i = pyfunc_v_i
    f.prop_f_s_i = pyfunc_s_i
    f.prop_f_s_o = pyfunc_s_o
    f.prop_f_s_b = pyfunc_s_o
    f.prop_f_i_s = pyfunc_i_s
    self.assertTrue(f.call_funcs())


class TestPythonBindingsParameters (unittest.TestCase):
  @classmethod
  def setUpClass (cls):
    _configure()


  def test_optional_arguments (self):
    # Test optional arguments

    self.assertEqual(f.f_opt_i(), 4)
    self.assertEqual(f.f_opt_i(4), 16)

    self.assertEqual(f.f_opt_s(), "hi")
    self.assertEqual(f.f_opt_s("bye"), "bye")
    self.assertIs(f.f_opt_s(None), None)


  def test_overloading (self):
    # Test overloading

    self.assertEqual(f.f_over(), "Nothing")
    self.assertEqual(f.f_over(32), "Int32")
    self.assertEqual(f.f_over("x"), "String")
    self.assertEqual(f.f_over(None), "String")
    self.assertEqual(f.f_over(32,"x"), "Int32,String")
    self.assertEqual(f.f_over(32,None), "Int32,Object")
    self.assertEqual(f.f_over(32,b), "Int32,Object")

  def test_global_method_overloading_on_instance (self):
    self.assertEqual(f.gf_overload(), "Overload1")
    self.assertEqual(f.gf_overload(1), "Overload2")

  def test_global_method_overloading_on_class (self):
    self.assertEqual(Foo.gf_overload(), "Overload1")
    self.assertEqual(Foo.gf_overload(1), "Overload2")


class TestPythonBindingsExceptions (unittest.TestCase):
  @classmethod
  def setUpClass (cls):
    _configure()


  def test_rogue_code_exception (self):
    # Test Rogue code that raises exception
    assertRR = getattr(self, "assertRaisesRegex", lambda a,b,c: self.assertRaises(a,c))

    assertRR(RuntimeError, ".*This is from Rogue.*", f.f_rogue_exception)


  def test_python_code_exception (self):
    # Test Rogue calling Python function that raises exception

    def pyfunc ():
      raise RuntimeError("This is from Python")

    f.prop_f_exception = pyfunc

    s = f.f_python_exception()
    self.assertTrue("This is from Python" in s)


class TestPythonCompounds (unittest.TestCase):
  @classmethod
  def setUpClass (cls):
    _configure()

  def test_python_compound_create (self):
    x = MyCompound.create()
    self.assertEqual(x.cp_int, 43)

    x = MyCompound.create(1,2,"3")
    self.assertEqual(x.cp_int, 1)

  def test_python_compound_create2 (self):
    x = MyCompound.create()

    x.cp_int = 4900
    self.assertEqual(x.cp_int, 4900)
    x.cp_str = "Test123"
    self.assertEqual(x.cp_str, "Test123")
    x.cp_str = None
    self.assertEqual(x.cp_str, None)

  def test_python_compound_global_property (self):
    # Tests accessing properties which are compounds
    self.assertTrue(Foo.gprop_comp.cp_real, 22)
    f.gprop_comp.cp_real = 23 # Shouldn't work! (Only changes temporary)
    self.assertTrue(Foo.gprop_comp.cp_real, 22)

    x = f.gprop_comp
    x.cp_real = 898.1
    f.gprop_comp = x
    self.assertTrue(Foo.gprop_comp.cp_real, 898.1)

  def test_python_compound_property (self):
    # Tests accessing properties which are compounds
    self.assertTrue(f.prop_comp.cp_str, "ok")

    f.prop_comp = f.gprop_comp
    self.assertTrue(f.prop_comp.cp_str, "okay")

  def test_python_method_returns_compound (self):
    f.prop_str = "fruitbat"
    x = f.f_compound_return()
    self.assertEqual(x.cp_str, "fruitbat")

  def test_python_method_takes_compound (self):
    x = f.gprop_comp
    x.cp_int += 1
    v = x.cp_int
    r = f.f_take_compound(x)
    self.assertEqual(v, r)

  def test_python_global_method_compounds (self):
    Foo.gprop_int = 0

    x = MyCompound.create(100,100,"100")
    y = Foo.gf_compound(x)

    self.assertEqual(Foo.gprop_int, 100)
    self.assertEqual(x.cp_int, 100)
    self.assertEqual(y.cp_int, 101)

  def test_python_method_on_compound (self):
    x = f.gprop_comp
    x.cp_int = 99
    x.cp_real = 0.5
    self.assertEqual(x.f_c_sum(), 99.5)

  def test_python_global_method_on_compound_no_compound (self):
    x = f.gprop_comp
    self.assertEqual(x.gf_int(3), 4)

    self.assertEqual(MyCompound.gf_int(9), 10)

  def test_python_global_method_on_compound (self):
    x = f.gprop_comp
    self.assertEqual(x.gf_compound(x, 9), 9 + f.gprop_comp.cp_int)

    self.assertEqual(MyCompound.gf_compound(x, 9), 9 + f.gprop_comp.cp_int)


if __name__ == "__main__":
  unittest.main()
