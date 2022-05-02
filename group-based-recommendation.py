import csv
import copy

#to save group scores
group_score = [[0 for col in range(6)] for row in range(10)]

#count number of places
place_num = -1#number of places 첫줄은 분류라 -1시작 
with open('place.csv', 'r') as f_p:
    reader_p = csv.reader(f_p)
    for i in reader_p:
        place_num += 1
    
#make group score with their members' scores
with open('group.csv', 'r') as f_g:
    reader_g = csv.reader(f_g)
    group_num = -1 #cuz first line does not contain group.
    for temp_g in reader_g:
        #find 'group'
        if "group" in temp_g[0]:
            group_score[group_num][0] = temp_g[0]
            for i in temp_g:
                #i == member of the group
                cnt = 0
                with open('member.csv', 'r') as f_m:
                    reader_m = csv.reader(f_m)
                    for temp_m in reader_m:
                        if i == temp_m[0]:#if you find the member
                            #개인 score을 하나씩 입력
                            
                            for j in range (1, 6):
                                #put weight on each criteria
                                if not temp_m[j] == '':
                                    if cnt == 0:#pin click*1
                                        group_score[group_num][j] += int(temp_m[j])
                                    elif cnt == 1:#detailed page*1.5
                                        group_score[group_num][j] += 1.5*int(temp_m[j])
                                    elif cnt == 2:#reservation*2
                                        group_score[group_num][j] += 2*int(temp_m[j])
                                    elif cnt == 3:#revisit*2.5
                                        group_score[group_num][j] += 2.5*int(temp_m[j])
                                    elif cnt == 4:#favorite*3
                                        group_score[group_num][j] += 3*int(temp_m[j])
                                
                            cnt += 1
        group_num += 1


#optimize the number of groups
group_score_op = [[group_score[row][col] for col in range(6)] for row in range(group_num)]
print(group_score_op)
#to save results by each system
rank_rule_allgroup = [['' for col in range(place_num+1)] for row in range(group_num)]
rank_item_allgroup = [['' for col in range(place_num+1)] for row in range(group_num)]
rank_user_allgroup = [['' for col in range(place_num+1)] for row in range(group_num)]
rank_final_allgroup = [['' for col in range(place_num+1)] for row in range(group_num)]

#member count dict for user based collaborative
member_cnt = {group_score_op[i][0]:0 for i in range(group_num)}





#Item based collaborative - search the most similar place
for g in range(group_num):
    #move in to dic and sort
    d_yet = {"chicken&beer":group_score_op[g][1], "soju":group_score_op[g][2], "pasta&wine":group_score_op[g][3], "whiskey":group_score_op[g][4], "kimbop":group_score_op[g][5]}
    #sort
    d_rule = sorted(d_yet.items(), key=lambda x: x[1], reverse=True)

    #Item based collaborative
    with open('place.csv', 'r') as f_p2:
        reader_p2 = csv.reader(f_p2)
        d_item = d_rule.copy()
        for temp_p2 in reader_p2:
            if temp_p2[0] == d_rule[0][0]: #when you find your most prefered place
                for key in d_rule:#temp_p2[1] is the most similar place, and gotta find it in the dic list for its score
                    if temp_p2[1] == key[0]:
                        d_item[0] = key
                        break
                cnt = 0
                #print(cnt, d_item)
            
                for key1 in d_item:
                    if cnt == 0:#skip 0, cuz we intentionally placed it right up there with the most similar place
                        cnt += 1
                        continue
                    for key2 in d_rule:
                        #print(key2)
                        #앞에 없는 거 확인. 그래야 중복 안 됨
                        test = True
                        for i in range(cnt):
                            if d_item[i] == key2:
                                test = False
                        if test == False:
                            continue# to the next d_rule to put in this d_item
                        else:
                            d_item[cnt] = key2
                            break# to the next d_item to fill in
                    #print(cnt, d_item)
                    cnt += 1
                    

    #results put in neatly // user not yet
    rank_rule_allgroup[g][0] = group_score_op[g][0]
    rank_item_allgroup[g][0] = group_score_op[g][0]
    for i in range(place_num):
        rank_rule_allgroup[g][i+1] = d_rule[i][0]
        rank_item_allgroup[g][i+1] = d_item[i][0]





rank_user_allgroup = copy.deepcopy(rank_rule_allgroup)

#User Based Collaborative
for g in range(group_num):



#search the most similar group by member
    for i in range(group_num):#initialize
        member_cnt[group_score_op[i][0]] = 0
    with open('group.csv', 'r') as f_g2:
        reader_g2 = csv.reader(f_g2)
        d_user = d_rule.copy()#여기에 추가하는거.
    
    #search the most similar group by member / 두번 sorting을 마쳤기 때문에 새로 훑자.
        for temp_g2 in reader_g2:
            if group_score_op[g][0] == temp_g2[0]:#when group name found in group.
            #get the members
                cnt = 0
                for member in temp_g2:#어차피 group name은 중복 안돼서 count 안되니까 걱정 ㄴ
                    if cnt == 0:#group name skip
                        #print('\ngroup', member) #if group name, print it
                        cnt += 1
                        continue
                    with open('group.csv', 'r') as f_g3:
                        reader_g3 = csv.reader(f_g3)
                        for temp_g3 in reader_g3:
                            if temp_g3[0] == group_score_op[g][0]:#기준이 되는 group일 때 넘어간다.
                                continue
                            elif member in temp_g3 and member != '':#member in the group and null skip
                                #print(temp_g3[0], member)
                                member_cnt[temp_g3[0]] += 1
                                
                    cnt += 1
        
        #sort the member_cnt
        member_cnt_srt = sorted(member_cnt.items(), key=lambda x: x[1], reverse=True)
        #print(member_cnt_srt)
        #member_cnt_srt[0][0] is the most similar group
        #print('similar group is', member_cnt_srt[0][0], '\n')


#find the similar group's favorite place in d_rule 지금 d_rule에는 현재 그룹의 place, score만 들어가있음.
    for i in range(group_num):
        if rank_rule_allgroup[i][0] == member_cnt_srt[0][0]:#similar group found
            if rank_rule_allgroup[i][1] == rank_user_allgroup[g][1]:#if their favorite place is the same
                                #apply 2nd favorite 
                j = rank_rule_allgroup[g].index(rank_rule_allgroup[i][2])
                for k in range(2, j+1):
                    rank_user_allgroup[g][k] = rank_rule_allgroup[g][k-1]#starts with j, cuz k starts as 2
                rank_user_allgroup[g][1] = rank_rule_allgroup[i][2]
            else:
                j = rank_rule_allgroup[g].index(rank_rule_allgroup[i][1])#j: recommend할 place의 기준 group에서의 rank
                for k in range(2, j+1):
                    rank_user_allgroup[g][k] = rank_rule_allgroup[g][k-1]#starts with j, cuz k starts as 2
                rank_user_allgroup[g][1] = rank_rule_allgroup[i][1]


                
                
            


#apply all at once
#1st-item based, 2nd-rule based, 3rd-user based
#item based를 기본으로 user based만 3rd place에 적용하면 됨
#member_cnt_srt[0][0]에 지금 group (g) 의 similar group 있음.
#d_user 에는 score 없음. d_rule, d_item loop다 끝나고 만들어서 못함. 대신 rank_rule_allgroup에 저장된 순위 이용함.
    rank_final_allgroup = copy.deepcopy(rank_item_allgroup)

    for i in range(group_num):
        if rank_user_allgroup[i][0] == member_cnt_srt[0][0]:#similar group found
            if rank_rule_allgroup[i][1] == rank_item_allgroup[g][1] or rank_rule_allgroup[i][1] == rank_item_allgroup[g][2]:#the similar's favorite is 1st or 2nd
                if rank_rule_allgroup[i][2] == rank_item_allgroup[g][1] or rank_rule_allgroup[i][2] == rank_item_allgroup[g][2]:#the similar's 2nd favorite is 1st or 2nd
                    j = rank_item_allgroup[g].index(rank_rule_allgroup[i][3])
                    for k in range(4, j+1):
                        rank_final_allgroup[g][k] = rank_item_allgroup[g][k-1]#3->4, 4->5
                    rank_final_allgroup[g][3] = rank_rule_allgroup[i][3]#put similar's in the final's 3rd
                    '''print('3')
                    print(rank_rule_allgroup[i])
                    print(rank_item_allgroup[g])
                    print(rank_final_allgroup[g])'''
                else:
                    j = rank_item_allgroup[g].index(rank_rule_allgroup[i][2])
                    for k in range(4, j+1):
                        rank_final_allgroup[g][k] = rank_item_allgroup[g][k-1]
                    rank_final_allgroup[g][3] = rank_rule_allgroup[i][2]
                    '''print('2')
                    print(rank_rule_allgroup[i])
                    print(rank_item_allgroup[g])
                    print(rank_final_allgroup[g])'''
            else:
                j = rank_item_allgroup[g].index(rank_rule_allgroup[i][1])
                for k in range(4, j+1):
                    rank_final_allgroup[g][k] = rank_item_allgroup[g][k-1]
                rank_final_allgroup[g][3] = rank_rule_allgroup[i][1]
                '''print('1')
                print(rank_rule_allgroup[i])
                print(rank_item_allgroup[g])
                print(rank_final_allgroup[g])'''
                
    



#output by group
for i in range(group_num):
    print(rank_rule_allgroup[i][0], '\n')
    print('Rule Based System')
    for j in range(place_num):
        print(j+1, ':', rank_rule_allgroup[i][j+1])
    print('RBS + Item Based Collaborative')
    for j in range(place_num):
        print(j+1, ':', rank_item_allgroup[i][j+1])
    print('RBS + User Based Collaborative')
    for j in range(place_num):
        print(j+1, ':', rank_user_allgroup[i][j+1])
    print('Final Recommendation System')
    for j in range(place_num):
        print(j+1, ':', rank_final_allgroup[i][j+1])
    print('\n')
