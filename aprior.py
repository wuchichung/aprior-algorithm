from collections import defaultdict
import itertools
import math

FILE_PATH = "./asso.csv"
N = 1000
MIN_SUP = int(0.1 * N)
MIN_CONF = 0.9
DEBUG = False


def get_transaction():
    with open(FILE_PATH) as f:
        for line in f.readlines():
            row = line.rstrip("\n").split(",")
            yield set(map(int, row[1:]))


def get_support(itemsets):
    result = [0 for _ in range(len(itemsets))]
    for tranction in get_transaction():
        for item_index, item in enumerate(itemsets):
            result[item_index] += int(set(item).issubset(tranction))
    return result


def get_new_candidate(items, prefix=None):
    new_items = []

    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            new_item = []
            if prefix:
                new_item = prefix
            new_item.extend([items[i], items[j]])

            new_items.append(new_item)

    return new_items


def get_all_subset(items):

    for i in range(0, math.ceil(len(items) / 2)):
        for subset in itertools.combinations(items, i + 1):
            yield subset


def main():
    ## get all the 1-candidate itemset
    candidate_itemset = set()
    for t in get_transaction():
        candidate_itemset.update(t)
    candidate_itemset = sorted(list(candidate_itemset))
    candidate_itemset = [[c] for c in candidate_itemset]

    ## use to store the support of frequence itemset
    frequent_itemset = {}

    ##
    prefix_length = 0

    ##
    if DEBUG:
        print("=" * 100)
        print("Find Frequent Itemsets")
        print("=" * 100)

    while len(candidate_itemset):
        if DEBUG:
            print("-" * 100)
            print("C:\n", candidate_itemset)

        ## get supports of candidate
        supports = get_support(candidate_itemset)
        if DEBUG:
            print("supp:\n", supports)

        ##
        for i in range(len(candidate_itemset) - 1, -1, -1):
            if supports[i] < MIN_SUP:
                ## remove item with support less than MIN_SUP
                candidate_itemset.pop(i)
            else:
                ## else store the support of this frequent item
                frequent_itemset.update({tuple(candidate_itemset[i]): supports[i]})

        if DEBUG:
            print("F:\n", candidate_itemset)

        ## build the new candidate itemsets
        if len(candidate_itemset):

            if len(candidate_itemset[0]) == 1:
                unpack_candidate_itemset = []
                for c in candidate_itemset:
                    unpack_candidate_itemset.extend(c)

                candidate_itemset = get_new_candidate(unpack_candidate_itemset)

            else:
                ##
                groups = defaultdict(list)
                for item in candidate_itemset:
                    groups[tuple(item[:prefix_length])].append(item[prefix_length])

                ##
                candidate_itemset = []
                for prefix_tuple, members in groups.items():
                    if len(members) >= 2:
                        candidate_itemset.extend(
                            get_new_candidate(members, prefix=list(prefix_tuple))
                        )

            ## increment prefix length
            prefix_length += 1

    ##
    print()
    print("=" * 100)
    print("Calculate Confidence")
    print("=" * 100)

    for itemset, count in frequent_itemset.items():
        if len(itemset) >= 2:
            for s in get_all_subset(itemset):
                ## find the complement itemset
                completement_s = tuple(sorted(list(set(itemset) - set(s))))
                ## calculate the confidence
                confidence = count / frequent_itemset[s]
                ## display message
                if DEBUG or (confidence > MIN_CONF):
                    print(
                        f"supp({s} U {completement_s}) : {count},",
                        f"supp({s}) : {frequent_itemset[s]},",
                        f"conf({s} -> {completement_s}) : {confidence:.3f}",
                    )


if __name__ == "__main__":
    main()
