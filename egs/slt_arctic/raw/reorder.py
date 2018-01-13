import os
import shutil
import sys
import struct
import numpy as np
from scipy import signal


def read_binary_file(filename, dimension=None):
    """Read data from matlab binary file (row, col and matrix).

    Returns:
        A numpy matrix containing data of the given binary file.
    """
    if dimension is None:
        read_buffer = open(filename, 'rb')

        rows = 0; cols= 0
        rows = struct.unpack('<i', read_buffer.read(4))[0]
        cols = struct.unpack('<i', read_buffer.read(4))[0]

        tmp_mat = np.frombuffer(read_buffer.read(rows * cols * 4), dtype=np.float32)
        mat = np.reshape(tmp_mat, (rows, cols))

        read_buffer.close()

        return mat
    else:
        fid_lab = open(filename, 'rb')
        features = np.fromfile(fid_lab, dtype=np.float32)
        fid_lab.close()
        assert features.size % float(dimension) == 0.0,'specified dimension %s not compatible with data'%(dimension)
        features = features[:(dimension * (features.size // dimension))]
        features = features.reshape((-1, dimension))

        return features


def write_binary_file(data, output_file_name, with_dim=False):
    data = np.asarray(data, np.float32)
    fid = open(output_file_name, 'wb')
    if with_dim:
        fid.write(struct.pack('<i', data.shape[0]))
        fid.write(struct.pack('<i', data.shape[1]))
    data.tofile(fid)
    fid.close()


if __name__ == '__main__':

    shutil.move('prepared_cmp','prepared_cmp_old')
    os.mkdir('prepared_cmp')

    for line in os.listdir('prepared_cmp_old'):
        filename, _ = os.path.splitext(line.strip())
        print('processing ' + filename)
        sys.stdout.flush()
        cmp_mat = read_binary_file(
            os.path.join('prepared_cmp_old', filename + '.cmp'), dimension=75)
        cmp_context_mat = np.zeros([cmp_mat.shape[0], 75])
        cmp_context_mat[:,    : 60] = cmp_mat[:,    : 60]
        cmp_context_mat[:, 60 : 65] = cmp_mat[:, 70 :   ]
        cmp_context_mat[:, 65     ] = cmp_mat[:, 60     ]
        cmp_context_mat[:, 66 :   ] = cmp_mat[:, 61 : 70]
        write_binary_file(
            cmp_context_mat[:, :],
            os.path.join('prepared_cmp', filename + '.cmp'))

