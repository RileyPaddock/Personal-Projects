def find_reduction(seq, marked_indices = []):
  seq = list(seq)
  if len(seq)<3 or seq == "":
      marked_indices = []
      return ''.join(seq)
  else:

    for i in range(len(seq)-2):
      if (seq[i]+seq[i+1]+seq[i+2] == "aaa") or (seq[i]+seq[i+1]+seq[i+2] == "bbb"):
        print("1")
        copy = [seq[j] for j in range(len(seq)) if j not in [i,i+1,i+2]]
        return find_reduction(copy)

    for i in range(len(seq)):
      if i+2<len(seq) and ((seq[i]+seq[i+1]+seq[i+2] == "aba") and ([i,i+1,i+2] not in marked_indices)):
        print("2")
        copy = list(seq)
        copy[i] = "b"
        copy[i+1] = "a"
        copy[i+2] = "b"
        marked_indices.append([i,i+1,i+2])
        return find_reduction(copy, marked_indices)
      elif (i+2)<len(seq) and ((seq[i]+seq[i+1]+seq[i+2] == "bab") and ([i,i+1,i+2] not in marked_indices)):
        print("3")
        copy = list(seq)
        copy[i] = "a"
        copy[i+1] = "b"
        copy[i+2] = "a"
        marked_indices.append([i,i+1,i+2])
        return find_reduction(copy, marked_indices)
      elif (i+5)<len(seq)and (seq[i]+seq[i+1]+seq[i+2]+seq[i+3]+seq[i+4]+seq[i+5] == ["a","a","b","b","a","a"]) and ([i,i+1,i+2,i+3,i+4,i+5] not in marked_indices):
        print("4")
        copy = list(seq)
        copy[i] = "b"
        copy[i+1] = "b"
        copy[i+2] = "a"
        copy[i] = "a"
        copy[i+1] = "b"
        copy[i+2] = "b"
        marked_indices.append([i,i+1,i+2, i+3, i+4, i+5])
        return find_reduction(copy, marked_indices)
      elif (i+5)<len(seq)and (seq[i]+seq[i+1]+seq[i+2]+seq[i+3]+seq[i+4]+seq[i+5] == ["b","b","a","a","b","b"]) and ([i,i+1,i+2,i+3,i+4,i+5] not in marked_indices):
        print("5")
        copy = list(seq)
        copy[i] = "a"
        copy[i+1] = "a"
        copy[i+2] = "b"
        copy[i] = "b"
        copy[i+1] = "a"
        copy[i+2] = "a"
        marked_indices.append([i,i+1,i+2, i+3, i+4, i+5])
        return find_reduction(copy, marked_indices)
    else:
      print("6")
      print(marked_indices)
      marked_indices = []
      return ''.join(seq)

def duplicator(string,num):
  duplicate = ""
  for _ in range(num):
    duplicate+=string

  return duplicate

one = ["","aab", "aba", "aabaab", "aabaabaab", "abaabaaba", "abaaab", "aababa"]
two = ["a"+x for x in one]
three = ["a"+y for y in two]
dicyclic = one+two+three



print(find_reduction(duplicator('aba',4)))

print(find_reduction(duplicator('aab',4)))


