def mathematical_calculation(example):
    ex = example.replace("^2", "**2")
    answer = eval(ex)
    answer = str(answer)
    
    return answer
