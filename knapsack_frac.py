def knapsack_frac(items, capacity):

    #intializing value/weight table of all items
    vw_table=[]     
    v_table=[]
    capacity2=capacity

    for i in range(len(items)):
        #adding each item along with its value by weight ratio
        vw_table+=[(items[i],items[i].value/items[i].weight)]
        v_table+=[(items[i],items[i].value)]
    
    #sorting based on the value by weight ratio
    vw_table=sorted(vw_table,key=lambda x:x[1],reverse=True)
    v_table=sorted(v_table,key=lambda x:x[1],reverse=True)

    included_items_vw=[]
    tot_val_vw=0
    tot_weight_vw=0

    #checking whether the item is divisible or can be packed inside the box
    for i in vw_table:
        item_weight=i[0].weight
        if item_weight<=capacity:
            capacity-=item_weight
            tot_weight_vw+=item_weight
            included_items_vw+=[i[0]]
            tot_val_vw+=i[0].value
        else: 
            if i[0].type=='Divisible':
                tot_weight_vw+=capacity
                
                tot_val_vw+=(i[1]*capacity)
                break
        
    vw_output=(tot_val_vw,included_items_vw,tot_weight_vw)

    included_items_v=[]
    tot_val_v=0
    tot_weight_v=0

    for i in v_table:
        item_weight=i[0].weight
        if item_weight<=capacity2:
            capacity2-=item_weight
            tot_weight_v+=item_weight
            included_items_v+=[i[0]]
            tot_val_v+=i[0].value
        else: 
            if i[0].type=='Divisible':
                tot_weight_v+=capacity2
            
                tot_val_v+=((i[1]/i[0].weight)*capacity2)
                break
    
    #returning result
    v_output=(tot_val_v,included_items_v,tot_weight_v)

    result=max(v_output,vw_output)

    notincluded=[]
    for i in items:
        if i not in result[1]:
            notincluded.append(i)

    print(result)
    return result,notincluded

if __name__=='__main__':
    from adt import item
    i1=item('fan',10,60,'InDivisible')
    i2=item('car',20,100,'Divisible')
    i3=item('bike',30,120,'InDivisible')
    l=[i1,i2,i3]
    result=knapsack_frac(l,50)
