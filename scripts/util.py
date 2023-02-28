import re
import os
import stat

RD, WD, XD = 4, 2, 1
BNS = [RD, WD, XD]
MDS = [
    [stat.S_IRUSR, stat.S_IRGRP, stat.S_IROTH],
    [stat.S_IWUSR, stat.S_IWGRP, stat.S_IWOTH],
    [stat.S_IXUSR, stat.S_IXGRP, stat.S_IXOTH]
]


def chmod(path, mode):
    if isinstance(mode, int):
        mode = str(mode)
    if not re.match("^[0-7]{1,3}$", mode):
        raise Exception("mode does not conform to ^[0-7]{1,3}$ pattern")
    mode = "{0:0>3}".format(mode)
    mode_num = 0
    for midx, m in enumerate(mode):
        for bnidx, bn in enumerate(BNS):
            if (int(m) & bn) > 0:
                mode_num += MDS[bnidx][midx]
    os.chmod(path, mode_num)


if __name__ == '__main__':
    chmod("xxx.sh", "744")  # 744代表所有者读写执行，组和其他的权限只有读
