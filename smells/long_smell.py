def calculate_tax(income):
    if income < 10000:
        tax = income * 0.1
    elif income < 50000:
        tax = income * 0.2
    elif income < 100000:
        tax = income * 0.3
    else:
        tax = income * 0.4
        
    deductions = 0
    if income > 50000:
        deductions += 5000
    if income > 100000:
        deductions += 10000
        
    tax -= deductions
    
    if income < 10000:
        tax = income * 0.1
    elif income < 50000:
        tax = income * 0.2
    elif income < 100000:
        tax = income * 0.3
    else:
        tax = income * 0.4
        
    deductions = 0
    if income > 50000:
        deductions += 5000
    if income > 100000:
        deductions += 10000
        
    tax -= deductions
    

    if income < 10000:
        tax = income * 0.1
    elif income < 50000:
        tax = income * 0.2
    elif income < 100000:
        tax = income * 0.3
    else:
        tax = income * 0.4
        
    deductions = 0
    if income > 50000:
        deductions += 5000
    if income > 100000:
        deductions += 10000
        
    tax -= deductions
    
    if income < 10000:
        tax = income * 0.1
    elif income < 50000:
        tax = income * 0.2
    elif income < 100000:
        tax = income * 0.3
    else:
        tax = income * 0.4
        
    deductions = 0
    if income > 50000:
        deductions += 5000
    if income > 100000:
        deductions += 10000
        
    tax -= deductions
    
    return tax

calculate_tax(50)
def process_data(data):
    result = []
    for record in data:
        if record.get('status') == 'active':
            if record.get('value') > 10:
                for i in range(5):
                    result.append(record)
                    print(f"Processed {len(result)} records.")
    return result
