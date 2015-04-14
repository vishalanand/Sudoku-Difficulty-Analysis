import numpy
import norvig

def conv_string_to_grid(string):
    matrix = numpy.zeros((9,9),dtype=numpy.int)
    for i in range(9):
        for j in range(9):
            # print (i)*9+j
            try:
                if string[(i)*9+j]!='.':
                    matrix[i][j]=int(string[(i)*9+j])
            except:
                print i*9+j
                print string[i*9+j]
    # print grid, string
    return matrix

def check_nonzero(listrc):
    already_present = [i for i in listrc if i!=0]
    return already_present

def add_unique_lists(list1,list2):
    # print list1, list2
    for i in list2:
        if i not in list1:
            list1.append(i)

    return list1

def get_els_grid(i,j,grid):
    # print i,j
    # print grid
    sets = [[0,1,2],[3,4,5],[6,7,8]]
    x = i/3
    y = j/3
    # print 'xy',x,y
    els = []
    count = 0
    for ind1 in sets[x]:
        for ind2 in sets[y]:
            count+=1
            if grid[ind1][ind2] not in els and grid[ind1][ind2]!=0:
                els.append(grid[ind1][ind2])
    # print 'els',els
    # print 'count',count
    return els

def get_candidates_matrix(grid):
    cands_count = numpy.full((9,9),9,dtype=numpy.int)
    for i in range(9):
        for j in range(9):
            # print i,j
            if grid[i][j] !=0:
                cands_count [i][j]=0
                continue
            cands = add_unique_lists(check_nonzero(grid[i,:]),check_nonzero(grid[:,j]))
            grid_els = get_els_grid(i,j,grid)
            cands = add_unique_lists(cands, check_nonzero(grid_els))
            cands_count [i][j]=9-len(cands)
            # print cands,9-len(cands)
    return cands_count

def count_params(string):
    matrix = conv_string_to_grid(string)
    params = {}
    params['num_givens'] = 81 - string.count('.')
    
    params ['3x3s_lowgivens'] = 0
    sets = [[0,1,2],[3,4,5],[6,7,8]]
    for i in range(9):
        x = i%3
        y = i/3
        count = 0
        for ind1 in sets[x]:
            for ind2 in sets[y]:

                if matrix[ind1][ind2]>0:
                    count+=1
        if count<=1:
            params['3x3s_lowgivens']+=1
    # print params['3x3s_lowgivens']

    params['numrows_lowgivens']=0
    params['numcols_lowgivens']=0
    rows_givens = []
    cols_givens = []
    # print numpy.nonzero(matrix)
    for i in range(9):
        count = (numpy.nonzero(matrix)[0] == i).sum()
        rows_givens.append(count)
    # print rows_givens
    for i in range(9):
        count = (numpy.nonzero(matrix)[1] == i).sum()
        cols_givens.append(count)
    # print cols_givens
    params['numrows_lowgivens'] = rows_givens.count(0)+rows_givens.count(1)
    params['numcols_lowgivens'] = cols_givens.count(0)+cols_givens.count(1)

    params['numdigits_lessthan3x'] = 0
    for i in range(1,10):
        if string.count(str(i))<3:
            params['numdigits_lessthan3x']+=1

    cands_count = get_candidates_matrix(matrix)
    params['numcells_2or1cand']= (cands_count == 1).sum() + (cands_count == 2).sum()
    return params

def convert_params_to_index(params, cutoffs):
    indices = []
    if params['num_givens']<cutoffs[0]:
        indices.append(0)
    else:
        indices.append(1)
    if params['3x3s_lowgivens']<=cutoffs[1]:
        indices.append(0)
    else:
        indices.append(1)
    if params['numrows_lowgivens']<=cutoffs[2]:
        indices.append(0)
    else:
        indices.append(1)
    if params['numcols_lowgivens']<=cutoffs[3]:
        indices.append(0)
    else:
        indices.append(1)
    if params['numdigits_lessthan3x']<=cutoffs[4]:
        indices.append(0)
    else:
        indices.append(1)
    if params['numcells_2or1cand']<=cutoffs[5]:
        indices.append(0)
    else:
        indices.append(1)
    return tuple(indices)

# type_sudokus = numpy.zeros((64,),dtype=numpy.int)

# pind = [1,0,1,0,0,1]
# print type_sudokus[tuple(pind)]
# print (type_sudokus == 0).sum()
[27-33]
0-3

list_cutoffs = [[30,1,1,1,1,3],[30,1,1,1,3,3]]


# for ct in list_cutoffs:    
for c1 in range(27,34):
    for c2 in range(0,4):
        for c3 in range(0,4):
            for c4 in range(0,4):
                for c5 in range(0,4):
                    for c6 in range(0,4):
                        ct = [c1,c2,c3,c4,c5,c6]
                        type_sudokus = numpy.zeros(shape=(2,2,2,2,2,2),dtype=numpy.int)
                        for i in range(25,41):
                            with open('sudokus/file'+str(i)+'.txt','r') as f:
                                for line in f:
                                    partial = line.split()[0]
                                    filled = line.split()[1]
                                    p = count_params(partial)
                                    # print p
                                    pind = convert_params_to_index(p, ct)
                                    type_sudokus[pind]+=1
                                    
                        count = 0
                        for i in type_sudokus.flatten():
                            if i<30:
                                count+=1
                        print ct,count
    

    # print type_sudokus.flatten()
# for i1 in [0,1]:
    #     for i2 in [0,1]:
    #         for i3 in [0,1]:
    #             for i4 in [0,1]:
    #                 for i5 in [0,1]:
    #                     for i6 in [0,1]:
    #                         if type_sudokus[i1,i2,i3,i4,i5,i6] <30:
    #                             print 'givens<',ct[0],i1,';3x3givens<',ct[1],i2,';rowslow<',ct[2],i3,';colslow<',ct[3],i4,';diglow<',ct[4],i5,';cands<',ct[5],i6, ';count: ', type_sudokus[i1,i2,i3,i4,i5,i6]
   