# own's
from boxcraft.controller import Box
from boxcraft.store import RedisStore
from boxcraft.exceptions import *
# third party's
from unittest import TestCase
from unittest.mock import patch
from os import environ
from time import sleep as time_sleep

def hello(instance=None, action=None):
    print(f"Action: {action} Instance: {instance}")

class TestBox(TestCase):

    store = RedisStore(
        host=environ.get('BOX_REDIS_HOST'),
        password=environ.get('BOX_REDIS_PASS')
    )

    # Store
    def test_store_connection(self):
        self.assertTrue(self.store)
    
    def test_store_failed_connection(self):
        with self.assertRaises(MissingGenericException):
            RedisStore(
                host='redis_store',
                password=environ.get('BOX_REDIS_PASS')
            )
    def test_store_failed_password_connection(self):
        with self.assertRaises(MissingGenericException):
            RedisStore(
                host=environ.get('BOX_REDIS_HOST'),
                password='password_testing'
            )

    def test_store_get_json_empty(self):
        self.assertEqual(self.store.get_json('test_get'), None)

    def test_store_set_and_get_json(self):
        example_json = {
            'keyA': "valueA",
            "listB": [
                {"keyC": "valueC"}
            ]
        }
        self.store.set_json('test_json', example_json)
        store_json = self.store.get_json('test_json')
        # clean
        self.store.connection.delete('test_json')
        self.assertEqual(store_json, example_json)

    # Boxes
    def test_box_task_delete(self):
        with patch('builtins.print'):
            tasks = { 'action': 'delete', 'name': 'poc-*', 'instances': str(["node-01", "node-02", "node-03", "node-04", "node-05"]) }
            ctx = Box()
            ctx.publish(tasks)
            # runner
            execution = False
            while True:
                # getting data
                task = ctx.getting()
                print(task)
                if task == None:
                    execution = True
                    break
                else:
                    print(f"Task: {task}")
                    ctx.runner(target=hello, kwargs={"instance": task['instances'], "action": task['action']})
                    time_sleep(2)
            self.assertEqual(execution, True)
    
    def test_box_task_create(self):
        with patch('builtins.print'):
            tasks = { 'action': 'create', 'name': 'poc', 'instances': "3" }
            ctx = Box()
            ctx.publish(tasks)
            # runner
            execution = False
            while True:
                # getting data
                task = ctx.getting()
                print(task)
                if task == None:
                    execution = True
                    break
                else:
                    print(f"Task: {task}")
                    ctx.runner(target=hello, kwargs={"instance": task['instances'], "action": task['action']})
                    time_sleep(2)
            self.assertEqual(execution, True)