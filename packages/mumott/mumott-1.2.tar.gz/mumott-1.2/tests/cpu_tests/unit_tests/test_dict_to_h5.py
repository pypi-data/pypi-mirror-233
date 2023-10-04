import pytest
from mumott.output_handling.saving import dict_to_h5

import numpy as np
import h5py


class myclass:
    a = 0


list_of_dicts = [dict(a=1, b=2, c=3),
                 dict(arr=np.array([0]), inner=dict(a=1, b=(1, 2, 3))),
                 dict(myst='stringstring', bst=b'bytestring', arr=np.array(['array', 'of', 'strings'])),
                 dict(co=1 + 1j, arr=np.array((1 + 1j)), ll=[np.array((1, 2)), np.array((4, 5))]),
                 dict(si=np.sin(np.pi / 5), sq=np.sqrt(2) / 10, sqrt=np.sqrt(3) * 1e-32),
                 dict(nope=None, dinope=dict(val=None)),
                 dict(arr=np.array([None])),
                 dict(myc=myclass())]

list_of_bools = [True, True, True, True, True, False, False, False]


def recursive_read(items, folder):
    for key, val in items.items():
        if isinstance(val, dict):
            recursive_read(val, folder[key])
        else:
            print(key, val, folder[key])
            # this monstrosity brought to you by encoding
            if np.array(val).dtype.kind in 'SU':
                if np.array(val).dtype.kind == 'S':
                    val = val.decode()
                if folder[key].size > 1:
                    for i in range(folder[key].size):
                        assert val[i] == folder[key][i].decode()
                else:
                    assert np.all(val == folder[key][0].decode())
            else:
                assert np.allclose(val, folder[key])


@pytest.mark.parametrize('in_dict, list_bool', [t for t in zip(list_of_dicts, list_of_bools)])
def test_saving(in_dict, list_bool, tmp_path):
    d = tmp_path / 'sub'
    d.mkdir()
    p = d / 'hello.h5'
    if list_bool is False:
        dict_to_h5(in_dict, p, True)
    else:
        dict_to_h5(in_dict, p, True)
        with h5py.File(p) as file:
            recursive_read(in_dict, file)
