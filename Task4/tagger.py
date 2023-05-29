# %%
import os
import sys
import numpy as np

# %%
def tag(training_list):
    # Tag the words from the untagged input file and write them into the output file.
    # Doesn't do much else beyond that yet.
    print("Tagging the file.")
    tags_set = set()
    words_set = set()
    tags_dict = dict()
    words_dict = dict()
    tags_len = 0
    words_len = 0
    for file_name in training_list:
        with open(file_name, encoding="utf8") as f:
            line = f.readline()
            while line != '':
                line_l = line.split()
                words_set.add(line_l[0])
                if len(words_set) != words_len:
                    words_dict[line_l[0]] = words_len
                    words_len += 1
                tags_set.add(line_l[2])
                if len(tags_set) != tags_len:
                    tags_dict[line_l[2]] = tags_len
                    tags_len += 1
                line = f.readline()
    initial_vector = np.zeros(len(tags_set), dtype='uint32')
    transition_matrix = np.zeros((len(tags_set), len(tags_set)), dtype='uint32')
    emission_matrix = np.zeros((len(tags_set), len(words_set)), dtype='uint32')
    dot_indx = words_dict['.']
    for file_name in training_list:
        with open(file_name, encoding="utf8") as f:
            starting = True
            line = f.readline()
            while line != '':
                word_str, _, tag_str = line.split()
                tag = tags_dict[tag_str]
                word = words_dict[word_str]
                if starting:
                    initial_vector[tag] += 1
                else:
                    transition_matrix[prev, tag] += 1                   
                emission_matrix[tag, word] += 1
                prev = tag
                starting = True if word == dot_indx else False
                line = f.readline()
    s = np.sum(initial_vector)
    initial_vector = np.divide(initial_vector, s)
    transition_matrix = transition_matrix.transpose()
    sum_vector = np.sum(transition_matrix, axis=0)
    transition_matrix = np.divide(transition_matrix, sum_vector).transpose()
    emission_matrix = emission_matrix.transpose()
    sum_vector = np.sum(emission_matrix, axis=0)
    emission_matrix = np.divide(emission_matrix, sum_vector).transpose()
    return (initial_vector, transition_matrix, emission_matrix, words_dict, tags_dict)

# %%
def viterbi(sentence, initial, transition, emission, words_dict):
    # sentence is list of words
    tags_n = initial.shape[0]
    words_n = len(sentence)
    sentence = [words_dict[i] if i in words_dict else -1 for i in sentence]
    prob = np.zeros((words_n, tags_n), 'float64')
    prev = np.ones((words_n, tags_n), 'float64') * (-1)
    first_prob = initial * (emission[:, sentence[0]]) if sentence[0] >= 0 else initial
    first_prob /= np.sum(first_prob)
    prob[0] = first_prob
    for n in range(1, words_n):
        for_prev = np.array([np.argmax(prob[n-1] * transition[:, i]) for i in range(tags_n)])
        # dont need emission matrix here because it's constant 
        word_probabilities = [1 for _ in range(tags_n)] if sentence[n] < 0 else emission[:, sentence[n]]
        for_prob = np.array([
            prob[n-1, for_prev[i]] * transition[for_prev[i], i] * word_probabilities[i] for i in range(tags_n)
            ])
        for_prob /= np.sum(for_prob)
        prev[n] = for_prev
        prob[n] = for_prob
    indx = -1
    current_tag = int(np.argmax(prob[indx]))
    path = []
    while current_tag >= 0:
        path.append(current_tag)
        current_tag = int(prev[indx, current_tag])
        indx -= 1
    path.reverse()
    return path

# %%
def test(test_file, output_file, train_output):
    initial_vector, transition_matrix, emission_matrix, words_dict, tags_dict = train_output
    tags_l = [0 for _ in range(len(tags_dict))]
    for k,v in tags_dict.items():
        tags_l[v] = k
    with open(test_file, 'r', encoding="utf8") as f_t, open(output_file, 'w', encoding="utf8") as f_o:
        sentence = []
        line = f_t.readline()[:-1]
        while line != '':
            sentence.append(line)
            if line == '.':
                path = viterbi(sentence, initial_vector, transition_matrix, emission_matrix, words_dict)
                lines = [ f"{sentence[i]} : {tags_l[path[i]]}\n" for i in range(len(sentence))]
                f_o.writelines(lines)
                sentence = []
            line = f_t.readline()[:-1]


# %%
if __name__ == '__main__':
    # Run the tagger function.
    print("Starting the tagging process.")

    # Tagger expects the input call: "python3 tagger.py -d <training files> -t <test file> -o <output file>"
    parameters = sys.argv
    training_list = parameters[parameters.index("-d")+1:parameters.index("-t")]
    test_file = parameters[parameters.index("-t")+1]
    output_file = parameters[parameters.index("-o")+1]
    # training_list = ["training1.txt"]
    # test_file = "test1.txt"
    # output_file = "output1.txt"
    # print("Training files: " + str(training_list))
    # print("Test file: " + test_file)
    # print("Output file: " + output_file)

    # Start the training and tagging operation.
    train_output = tag(training_list)
    test(test_file, output_file, train_output)


