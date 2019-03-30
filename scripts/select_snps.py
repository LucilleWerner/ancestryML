# module to select SNPS from AIM platforms
import os
import gzip
import random
from math import ceil

kgenome_dir = "/home/sevvy/Projects/aim_rf/Data/1000"
# kgenome_dir = "/home/sevvy/Projects/aim_rf/Data/test"
study_GAL = "/home/sevvy/Projects/aim_rf/Data/AIM/galanter_446.txt"
study_HAL = "/home/sevvy/Projects/aim_rf/Data/AIM/halder_175.txt"
study_panel = "/home/sevvy/Projects/aim_rf/Data/AIM/asfi_precpanel_165.txt"
study_meta = "/home/sevvy/Projects/aim_rf/Data/AIM/metatag.txt"
study_tendon = "/home/sevvy/Projects/aim_rf/Data/AIM/tandon_4325.txt"

GAL_snps = []
HAL_snps = []
panel_snps = []
meta_snps = []
tendon_snps = []

random_snps = [[], [], [], []]

studies = [study_GAL, study_HAL, study_panel, study_meta, study_tendon]
rs_studies = [[], [], [], [], []]
rs_lines = [[], [], [], [], []]

for i, study in enumerate(studies):
    with open(study, 'r') as opened:
        rs_ids = opened.read().splitlines()
        rs_ids = [x.strip() for x in rs_ids]
        rs_studies[i] = rs_ids

per_500 = ceil(500/22)
per_1000 = ceil(1000/22)
per_10000 = ceil(10000/22)
per_100000 = ceil(100000/22)


def count_lines(fpath):
    gz_opened = gzip.open(fpath, 'r')
    cnt = 0
    line = True
    while line:
        line = gz_opened.readline()

        line = line.decode('utf-8')

        if not line.startswith('#'):
            cnt += 1
    gz_opened.close()
    print('finished counting lines\n')
    return cnt


def generate_random(num_snps):
    random_nums = [[], [], [], []]
    for i, max in enumerate([per_500, per_1000, per_10000, per_100000]):
        for n in range(0, max):
            while True:
                random_num = random.randint(0, num_snps)
                if random_num not in random_nums[i]:
                    random_nums[i].append(random_num)
                    break
    return random_nums


def get_chr(filestring):
    chr = filestring[7:9]
    if chr[-1] == '.':
        chr = filestring[7:8]
    return chr


for vcf_file in os.listdir(kgenome_dir):
    fpath = os.path.join(kgenome_dir, vcf_file)
    print('starting SNP extraction on chromosome {}\n'.format(get_chr(vcf_file)))
    num_snps = count_lines(fpath)
    random_nums = generate_random(num_snps)
    gz_opened = gzip.open(fpath, 'r')

    cnt = 0
    line = True
    while line:
        line = gz_opened.readline()

        line = line.decode('utf-8')

        if not line.startswith('#') and line.strip():

            for i, numset in enumerate(random_nums):
                for num in numset:
                    if cnt == num:
                        random_snps[i].append(line)

            rs_id = line.split('\t')[2]

            # for i, study in enumerate(rs_studies):
            #     if rs_id in study:
            #         rs_lines[i].append(line)
            cnt += 1

    gz_opened.close()

data_dir = '/home/sevvy/PycharmProjects/ethgeno/data'
random_files = ['random500_1.txt', 'random1000_1.txt', 'random10000_1.txt', 'random1000000_1.txt']

for i, name in enumerate(random_files):
    out = open(os.path.join(data_dir, name), 'a')
    out.write(''.join(random_snps[i]))
    out.close()

for i, max in enumerate([per_500, per_1000, per_10000, per_100000]):
    many = len(random_snps[i]) - max
    for n in range(0, many):
        rand = random.randint(0, len(random_snps[i])-1)
        random_snps[i].pop(rand)

data_dir = '/home/sevvy/PycharmProjects/ethgeno/data'
random_files = ['random500.txt', 'random1000.txt', 'random10000.txt', 'random1000000.txt']

for i, name in enumerate(random_files):
    out = open(os.path.join(data_dir, name), 'a')
    out.write(''.join(random_snps[i]))
    out.close()

# study_files = ['GAL_snps.txt', 'HAL_snps.txt', 'panel_snps.txt', 'meta_snps.txt', 'tendon_snps.txt']
# for i, name in enumerate(study_files):
#     out = open(os.path.join(data_dir, name), 'a')
#     out.write(''.join(rs_lines[i]))
#     out.close()
