import sys
from selector import Grammar


samples = [
    # 'model1',
    # 'path:models',
    # 'model1 model2',
    # 'model1,model2',
    # 'model1,model2,model3',
    # 'model1,model2 model3',
    # '+model1',
    # 'model1+',
    # '+model1+', TODO: !
    # '@model1',
    # '(model1,model2)',
    # '((model1),((model2)))',
    # '(@model1,@model2),model3',
    # 'tag:abc',
    # 'tag:abc,tag:def',
    # 'tag:abc tag:def',
    # 'snowplow.*',
    # 'finance.base.*',
    'source:snowplow+',
    '@source:snowplow',
    '+tag:nightly+',
    'my_package.*+',
    'my_package.a_big_model+',
    # '((model1,model2),(model3,model4))'
]

grammar = Grammar()

for data in samples:
    result = grammar.parse(data, debug=False)
    print(result)
