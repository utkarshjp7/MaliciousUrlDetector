'''
Utkarsh Patel & Mayank Jain
CIS 475 Final Project
'''

import csv
import feature_extractor
import trainer as tr

def write_feature(feature, output_dest, write_header):
    with open(output_dest, 'ab') as f:
        w = csv.DictWriter(f, feature.keys())
        if write_header:
            w.writeheader()
        w.writerow(feature)

def generate_train_features(train_data_file, train_feature_file):
    write_header = True
    with open(train_data_file, 'rb') as csvfile:
        csvReader = csv.DictReader(csvfile)
        i = 0
        for row in csvReader:
            url = row['url']
            is_malicious = 1 if row['label'] == 'bad' else 0
            if url:
                urlFeature = feature_extractor.extract(url)
                urlFeature['malicious'] = is_malicious
                write_feature(urlFeature, train_feature_file, write_header)
                write_header = False
                i += 1
            if (i % 100) == 0:
                print "Processed {0} urls".format(i)

def generate_test_features(test_data_file, test_feature_file):
    write_header = True
    with open(test_data_file) as f:
        for line in f:
            url = line.split(',')[0].strip()
            if url:            
                urlFeature = feature_extractor.extract(url)
                write_feature(urlFeature, test_feature_file, write_header)
                write_feature = False


def main():
    generate_train_features('train_data.csv','train_features.csv')
    generate_test_features("test_data.txt",'test_features.csv')
    tr.train('train_features.csv', 'test_features.csv')     

if __name__ == "__main__":
    main()
