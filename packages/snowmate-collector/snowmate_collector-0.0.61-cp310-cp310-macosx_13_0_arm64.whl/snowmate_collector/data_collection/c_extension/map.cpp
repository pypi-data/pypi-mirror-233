#include <unordered_map>
#include <map>
#include "map.hpp"
#include "Python.h"
#include "tsl/robin_map.hpp"

tsl::robin_map<int, uint8_t> g_tid_to_currently_recording;
tsl::robin_map<PyObject *, int> g_func_to_counter;
tsl::robin_map<PyObject *, PyObject*> g_gen_to_metadata;
std::unordered_map<PyObject*,PyObject*> g_object_to_object;


/**
 * This function sets a mapping of a generator to its metadata
 * relevant for us. Usually a UserFunctionCall object.
 * 
 * @param key The generator object.
 * @param value The metadata object (mostly a UserFunctionCall object).
 * 				If 0 is passed, the mapping is deleted.
 * @return 0
 */
int _Py_HOT_FUNCTION set_gen_to_metadata(PyObject * key, PyObject * value)
{
	if (value == 0) {
		g_gen_to_metadata.erase(key);
		return 0;
	}
	(g_gen_to_metadata)[key] = value;
    return 0;
}

/**
 * This function returns the metadata object for a generator.
 * Usually the returned metadata object is a UserFunctionCall object.
 * 
 * @param key The generator object.
 * @return The metadata object (mostly a UserFunctionCall object).
 * 		   0 if no mapping exists.
 */
PyObject * _Py_HOT_FUNCTION get_gen_to_metadata(PyObject * key)
{
	
	auto pos = ((g_gen_to_metadata)).find(key);
	if (pos == ((g_gen_to_metadata)).end()) {
		return 0;
	} else {
		return pos->second;

	}
}

/**
 * This function sets a mapping of a thread id to its `g_currently_recording`.
 * 
 * @param key The thread id.
 * @param value The `g_currently_recording` value.
 * @return 0
 */
int _Py_HOT_FUNCTION set_tid_to_currently_recording(int key, uint8_t value)
{
	(g_tid_to_currently_recording)[key] = value;
    return 0;
}

/**
 * This function returns the `g_currently_recording` value for a thread id.
 * 
 * @param key The thread id.
 * @return The `g_currently_recording` value.
 * 		   0 if no mapping exists.
 */
uint8_t _Py_HOT_FUNCTION get_tid_to_currently_recording(int key)
{
	auto pos = ((g_tid_to_currently_recording)).find(key);
	if (pos == ((g_tid_to_currently_recording)).end()) {
		return 0;
	} else {
		return pos->second;

	}

}

/**
 * This function sets a mapping of a function object to its counter.
 * 
 * @param key The function object.
 * @param value The counter value.
 * @return 0
 */
int _Py_HOT_FUNCTION set_func_to_counter(PyObject * key, int value)
{
	(g_func_to_counter)[key] = value;
	return 0;
}

/**
 * This function returns the counter value for a function object.
 * 
 * @param key The function object.
 * @return The counter value.
 * 		   0 if no mapping exists.
 */
int __attribute__((hot)) __attribute__((always_inline))  _Py_HOT_FUNCTION get_func_to_counter(PyObject  * key)
{
	auto pos = ((g_func_to_counter)).find(key);
	if (pos == ((g_func_to_counter)).end()) {
		return 0;
	} else {
		return pos->second;
	}
}

int _Py_HOT_FUNCTION set_int_to_int_item(void * mapper, int key, int value)
{

	tsl::robin_map<int, int> * mapping_obj = (tsl::robin_map<int, int> *)mapper;
	(*mapping_obj)[key] = value;
	return 0;
}
int _Py_HOT_FUNCTION get_int_to_int_item(void * mapper, int key)
{
	tsl::robin_map<int, int> * mapping_obj = (tsl::robin_map<int, int> *)mapper;

	auto pos = (*mapping_obj).find(key);
	if (pos == (*mapping_obj).end()) {
		return 0;
	} else {
		return pos->second;

	}

}


int _Py_HOT_FUNCTION set_pyobject_to_pyobject_item(PyObject * key, PyObject * value)
{

	(g_object_to_object)[key] = value;
	return 0;
}
PyObject  _Py_HOT_FUNCTION * get_pyobject_to_pyobject_item(PyObject * key)
{
	auto pos = (g_object_to_object).find(key);
	if (pos == (g_object_to_object).end()) {
		return 0;
	} else {
		return pos->second;
	}

}
