import sys
from selector import Grammar


samples = [
    'model1',
    # 'path:models',
    # 'model1 model2',
    # 'model1,model2',
    # 'model1,model2,model3',
    # 'model1,model2 model3',
    # '+model1',
    # 'model1+',
    # '@model1',
    # '(model1,model2)',
    # '((model1),((model2)))',
    # '(@model1,@model2),model3',
    # 'tag:abc',
    # 'tag:abc,tag:def',
    # 'tag:abc tag:def',
    # 'snowplow.*',
    # 'finance.base.*',
    # 'source:snowplow+',
    # '@source:snowplow',
    # 'my_package.*+',
    # 'my_package.a_big_model+',
    # '((model1,model2),(model3,model4))',
    # 'model1+5',
    # 'model1+',
    # 'model1+0',
    # '0+model1',
    # '12+model1',
    # '3+model1+4',
    # '+tag:nightly+',
    # '+model1+',
]

grammar = Grammar()

for data in samples:
    result = grammar.parse(data, debug=False)
    print(result)
