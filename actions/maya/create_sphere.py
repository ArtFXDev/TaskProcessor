import pymel.core as pm

s = pm.polySphere(name={0}, radius={1})
{2} = str(s[0])

print("Sphere {} created".format({2}))