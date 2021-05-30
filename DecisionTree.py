import pandas as pd
import math

class Node:
    def __init__(self):

        self.name_column = None
        self.childs_names = None
        self.entropy = None
        self.childs_next = None
        self.decision = None

    def get_column_name(self):
        return self.name_column

    def get_childs_next(self):
        return self.childs_next

    def get_entropy(self):
        return self.entropy

    def get_childs_name(self):
        return self.childs_names

    def get_dicision(self):
        return self.decision

    def set_col_name(self, name):
        self.name_column = name

    def set_childs_next(self, childs):
        return self.childs_next

    def set_entropy(self, entro):
        return self.entropy

    def set_child_names(self, cn):
        self.childs_names = cn

    def set_dicsion(self, decision):
        self.decision = decision


class Decision_tree:
    def __init__(self):
        self.root = None
    '''
    This function is used to split data into training and test
    '''
    def split_train_test(self, df):
        num_of_rows = df.shape[0]
        number_for_80_persent = int((8/10)*num_of_rows)
        train_x = df.iloc[:number_for_80_persent, :len(df.columns)-1]
        train_y = df.iloc[:number_for_80_persent, len(df.columns)-1]

        test_x = df.iloc[number_for_80_persent:, :len(df.columns)-1]
        test_y = df.iloc[number_for_80_persent:, len(df.columns)-1]

        return train_x, train_y, test_x, test_y
    '''
    this function takes  data frame and return true or flase
    it returns true if table(data frame) is pure 
    '''
    def is_set_pure(self, data_frame):
        print('*** is pure  ****')
        y_lable = data_frame.iloc[:, -1]
        first_value = y_lable[0]
        pure_bool = True
        for value in y_lable:
            if first_value != value:
                pure_bool = False
                break
        print(pure_bool)
        print('*** is pure  end****')
        return pure_bool
    '''
    this function take the data frame and return the info gain of that table and also p,n values for that table
    '''
    def find_info_gain_of_tree(self, df):
        y_lable = df.iloc[:, -1]
        p = 0
        n = 0
        for value in y_lable:
            if value == 'yes':
                p = p+1
            else:
                n = n+1
       # info_gain = ((-p/(p+n))*(math.log((p/(p+n)), 2)))-((n/(p+n))*(math.log((n/(p+n)), 2)))
        info_gain = self.find_info_gain_of_(p, n)
        return info_gain, p, n
    '''
    this function takes  p and n values and compute the info gain for the giving p and n and returns the results
    '''
    def find_info_gain_of_(self, p, n):
        if p == 0 or n == 0:
            return 0
        info_gain = ((-p/(p+n))*(math.log((p/(p+n)), 2))) - ((n/(p+n))*(math.log((n/(p+n)), 2)))
        return info_gain
    '''
    this function finds the unigue values from a column
    '''
    def find_unique_elements(self, list_d):
        temp = []
        for value in list_d:
            if value not in temp:
                temp.append(value)
        return temp
    '''
    it takes x_column and y_label and make the entropy data frame for that column and returns it
    '''
    def find_info_gain_entropy(self, x, y):
        unique_set = self.find_unique_elements(x)
        df_e_t = pd.DataFrame(columns=['column_unique_values', 'pi', 'ni', 'info_gain'])
        for value in unique_set:
            pi = 0
            ni = 0
            for (xi, yi) in zip(x, y):
                if value == xi and yi == 'yes':
                    pi = pi + 1
                if value == xi and yi == 'no':
                    ni = ni + 1
            infogain = self.find_info_gain_of_(pi, ni)
            row = {'column_unique_values': value, 'pi': pi, 'ni': ni, 'info_gain': infogain}
            df_e_t = df_e_t.append(row, ignore_index=True)
        return df_e_t
    '''
    it takes the entropy table(data_frame) and p and n of that table and calculate the in entropy of that table
    using entropy formula
    '''
    def find_entropy(self, df_e, p, n):
        result = 0
        for rows in df_e.itertuples():
            print(rows[1], rows[2], rows[3])
            result = result + (rows[2]+rows[3])/(p+n)*rows[4]
        return result
    '''
    this function takes the information gain of table and entropy of column
    and return the gain for that table 
    '''
    def find_gain(self, info_gain, entropy):
        return info_gain - entropy
    def inset_intree(self,tem_node):
        if self.root == None:
            self.root = tem_node
        else:
            move = self.root
            while(move != None):
                for chil in move.get_childs_name():
                    if chil == move.get_column_name():
                        next_chiild_dic = move.get_childs_next()
                        next_chiild_dic[chil] = move

    def insert_decision(self, colname, decision):
        move = self.root
        while(move != None):
            for child in move.get_childs_name():
                if child == colname:
                    move.set_dicsion(decision)
                    break

    def find_decision(self, data_frame):
        dec = data_frame.iloc[:, -1]
        col = data_frame.iloc[0, 0]
        for d in dec:
            if dec == 'yes':
                return 'yes', col
            else:
                return 'no', col
    def display(self):
        print('**********************************************  display ************************')
        move = self.root
        while(True):
            if(move.get_dicision() == 'yes' or move.get_dicision() == 'no'):
                return
            else:
                print(move.get_column_name())
                print("Childs : ")
                for childs in move.get_childs_name():
                    print(childs)
                dics = move.get_childs_next()
                for value in dics.values():
                    print(value)
                print('**********************************************  display ************************')



    def fit(self, data_frame):
        print('******************************************   fit  start  ***********************************')
        self.real_df = data_frame
        if self.is_set_pure(data_frame):
            print("\n******   We Are in   ******   Base Case\n")
            print(data_frame)
            print('\n')
            print('***************************************************************************************************')
            print("\n\n\n")
            '''
            Stores these Values Some Where
            '''
            decs, col = self.find_decision(data_frame)
            self.insert_decision(col, decs)
            print('Decision : ', decs)
            print('Column name : ', col, '\n')
            return

        info_gain, p, n = self.find_info_gain_of_tree(data_frame)
        print("Info Gain of Table : ", info_gain)
        print("      p : ", p, ' n : ', n)
        gain_dic = {}
        for column_name in data_frame.iloc[:, :-1]:
            df_e_t = self.find_info_gain_entropy(data_frame[column_name], data_frame.iloc[:, -1])
            entropy = self.find_entropy(df_e_t, p, n)
            gain = self.find_gain(info_gain, entropy)
            gain_dic[column_name] = gain

        selected_column = max(zip(gain_dic.values(), gain_dic.keys()))
        selected_column_name = selected_column[1]
        column_values = data_frame[selected_column_name].tolist()
        column_childs = self.find_unique_elements(column_values)
        print('Selected Column Name : ', selected_column_name)
        print('Selected Column Childs : ', column_childs)

        '''
            Stores These Values Some Where
        '''
        temp_node = Node()
        temp_node.set_col_name(selected_column_name)
        temp_node.set_child_names(column_childs)
        self.inset_intree(temp_node)
        print('******************************************   fit  end  ***********************************')
        for col_val in column_childs:
            print("===================================    Data Frame  ================================")
            new_df = data_frame[data_frame[selected_column_name] == col_val]
            print(new_df)
            print("===================================    Data Frame  ================================")
            self.fit(new_df)

df = pd.read_csv('tenis_dataset.csv')

obj = Decision_tree()
obj.fit(df)
obj.display()







