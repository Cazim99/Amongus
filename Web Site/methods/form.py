from flask import flash

def is_submited(form):
    if len(form) > 0:
        return True
    return False

def check_form(form, inputs_rules, fromApplication=False):
    for input in inputs_rules.keys():
        if not input in form: 
            if fromApplication==False:
                flash(f"Something went wrong", "is-danger")
                return False
            else:  
                return f"Something went wrong"
        else:
            if inputs_rules[input]['same-check'] != None:
                if form[input] != form[inputs_rules[input]['same-check']]:
                    if fromApplication==False:
                        flash(f"{inputs_rules[input]['name']}s is not the same", "is-danger")
                        return False
                    else:
                        return f"{inputs_rules[input]['name']}s is not the same"
            
            if len(form[input]) <= inputs_rules[input]['min-len']:
                if fromApplication==False:
                    flash(f"{inputs_rules[input]['name']} must have more then {inputs_rules[input]['min-len']} characters", "is-danger")
                    return False
                else:
                    return f"{inputs_rules[input]['name']} must have more then {inputs_rules[input]['min-len']} characters"
            elif inputs_rules[input]['max-len'] != None:
                if len(form[input]) >= inputs_rules[input]['max-len']:
                    if fromApplication==False:
                        flash(f"{inputs_rules[input]['name']} cant be bigger then {inputs_rules[input]['max-len']} characters", "is-danger")
                        return False
                    else:
                        return f"{inputs_rules[input]['name']} cant be bigger then {inputs_rules[input]['max-len']} characters"
    return True
    
