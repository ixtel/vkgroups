#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys
import time
import requests
import pickle

from settings import token, my_id, api_v, max_workers

class VkException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class VkFriends():
    parts = lambda lst, n=25: (lst[i:i + n] for i in iter(range(0, len(lst), n)))
    make_targets = lambda lst: ",".join(str(id) for id in lst)

    def __init__(self, *pargs):
        try:
            self.token, self.my_id, self.api_v, self.max_workers = pargs
            self.my_name, self.my_last_name, self.photo = self.base_info([self.my_id])

        except VkException as error:
            sys.exit(error)

    def request_url(self, method_name, parameters, access_token=False):


        req_url = 'https://api.vk.com/method/{method_name}?{parameters}&v={api_v}'.format(
            method_name=method_name, api_v=self.api_v, parameters=parameters)

        if access_token:
            req_url = '{}&access_token={token}'.format(req_url, token=self.token)

        return req_url




    def base_info(self, ids):

        r = requests.get(self.request_url('users.get', 'user_ids=%s&fields=photo' % (','.join(map(str, ids)))))

        r = r.json()

        if 'error' in r.keys():
            raise VkException('Error message: %s Error code: %s' % (r['error']['error_msg'], r['error']['error_code']))
        r = r['response'][0]

        if 'deactivated' in r.keys():
            raise VkException("User deactivated")
        return r['first_name'], r['last_name'], r['photo']

    @staticmethod
    def save_load_deep_friends(myfile, sv, smth=None):
        if sv and smth:
            pickle.dump(smth, open(myfile, "wb"))
        else:
            return pickle.load(open(myfile, "rb"))

    def base_info2(self, ids):
        r = requests.get(self.request_url('users.get', 'user_ids=%s&fields=photo' % (','.join(map(str, ids))))).json()
        return r



if __name__ == '__main__':
    a = VkFriends(token, my_id, api_v, max_workers)
    print(a.my_name, a.my_last_name, a.my_id, a.photo)
    #print(a.common_friends())
    #df = a.deep_friends(deep)
    #print(df)
    #VkFriends.save_load_deep_friends('deep_friends_dct', True, df)
    #print(pickle.load( open('deep_friends_dct', "rb" )))
    #print(a.from_where_gender())
