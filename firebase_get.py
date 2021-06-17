from firebase import firebase
firebase = firebase.FirebaseApplication('https://research-paper-finder-default-rtdb.asia-southeast1.firebasedatabase.app/', None)

result = firebase.get('/', None)
print(result[0])