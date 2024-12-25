class A:
	pass

class B(A):
	pass

a = B().__class__.__bases__

print(a)