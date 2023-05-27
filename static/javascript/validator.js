// đối tượng Validator
function Validator(options) {
  function getParent(element, seletor) {
    while (element.parentElement) {
      if (element.parentElement.matches(seletor)) {
        return element.parentElement;
      }
      element = element.parentElement;
    }
  }
  var selectorRules = {};

  // hàm thực hiện validate
  function validate(inputElement, rule) {
    var errorElement = getParent(
      inputElement,
      options.formGroupSelector
    ).querySelector(options.errorSelector);
    var errMessage;

    // lấy ra các rules của selector
    var rules = selectorRules[rule.selector];

    // lặp qua từng rule & kiểm tra
    // nếu có lỗi thì dừng việc kiểm tra
    for (var i = 0; i < rules.length; i++) {
      switch (inputElement.type) {
        case "checkbox":
        case "radio":
          errMessage = rules[i](
            formElement.querySelector(rule.selector + ":checked")
          );
          break;
        default:
          errMessage = rules[i](inputElement.value);
      }
      if (errMessage) break;
    }

    if (errMessage) {
      errorElement.innerText = errMessage;
      getParent(inputElement, options.formGroupSelector).classList.add(
        "invalid"
      );
    } else {
      errorElement.innerText = "";
      getParent(inputElement, options.formGroupSelector).classList.remove(
        "invalid"
      );
    }
    return !errMessage;
  }

  // lấy element của form cần validate
  var formElement = document.querySelector(options.form);
  if (formElement) {
    // khi submit form
    formElement.onsubmit = function (e) {
      e.preventDefault();

      var isFormValid = true;

      // lặp qua từng rule và validate luôn
      options.rules.forEach(function (rule) {
        var inputElement = formElement.querySelector(rule.selector);
        var isValid = validate(inputElement, rule);
        if (!isValid) {
          isFormValid = false;
        }
      });

      // trong trường hợp các input hợp lệ
      if (isFormValid) {
        // trường hợp submit với javascript
        if (typeof options.onSubmit === "function") {
          var enableInputs = formElement.querySelectorAll("[name]");
          // conver nodelist sang array
          var formValues = Array.from(enableInputs).reduce((values, input) => {
            // values[input.id] = input.value
            switch (input.type) {
              case "checkbox":
                if (!input.matches(":checked")) {
                  values[input.name] = "";
                  return values;
                }
                if (!Array.isArray(values[input.name])) {
                  values[input.name] = [];
                }
                values[input.name].push(input.value);
                break;
              case "radio":
                values[input.name] = formElement.querySelector(
                  'input[name="' + input.name + '"]:checked'
                ).value;
                break;
              case "file":
                values[input.name] = input.files;
                break;
              default:
                values[input.id] = input.value;
            }
            return values;
          }, {});

          // call API để tạo dữ liệu
          // console.log(formValues);
          options.onSubmit(formValues);
        }

        // trường hợp submit mặc định với html
        else {
          formElement.submit();
        }
      }
    };

    // Lặp qua mỗi rule và xử lý (lắng nghe sự kiện)
    options.rules.forEach((rule) => {
      // lưu lại các Rule cho mỗi ô input4
      if (Array.isArray(selectorRules[rule.selector])) {
        selectorRules[rule.selector].push(rule.test);
      } else {
        selectorRules[rule.selector] = [rule.test];
      }

      var inputElements = formElement.querySelectorAll(rule.selector);
      Array.from(inputElements).forEach((inputElement) => {
        if (inputElement) {
          // xử lí khi blur khỏi ô input
          inputElement.onblur = function () {
            validate(inputElement, rule);
          };

          // xử lí mỗi khi người dùng nhập vào ô input
          inputElement.oninput = function () {
            var errorElement = getParent(
              inputElement,
              options.formGroupSelector
            ).querySelector(".form-message");
            errorElement.innerText = "";
            getParent(inputElement, options.formGroupSelector).classList.remove(
              "invalid"
            );
          };
        }
      });
    });
  }
}

// định nghĩa các qui tắc (yêu cầu)
// nguyên tắc các rule
// 1) khi có lỗi -> trả ra message lỗi
// 2) khi hợp lệ -> không trả cái gì cả
Validator.isRequired = function (selector, message) {
  return {
    selector,
    test(value) {
      return value.trim() ? undefined : message || "Please enter this field";
    },
  };
};
Validator.isRequiredGender = function (selector, message) {
  return {
    selector,
    test(value) {
      return value ? undefined : message || "Please choose your gender";
    },
  };
};
Validator.isEmail = function (selector, message) {
  return {
    selector,
    test(value) {
      var regex = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
      return regex.test(value)
        ? undefined
        : message || "This field must be email";
    },
  };
};

Validator.isMinLength = function (selector, min, message) {
  return {
    selector,
    test(value) {
      return value.length >= min
        ? undefined
        : message || `Password needs at least ${min} characters`;
    },
  };
};

Validator.isConfirmed = function (selector, getConfirmValue, message) {
  return {
    selector,
    test(value) {
      return value === getConfirmValue()
        ? undefined
        : message || `Input data does not match`;
    },
  };
};

function authen() {

}

Validator.isConfirmAcc = function (selector, getConfirmValue, message) {
  return {
    selector,
    test(value) {
      return value === getConfirmValue()
        ? undefined
        : message || `Please enter this field`;
    },
  };
};

Validator.isConfirmPass = function (selector, getConfirmValue, message) {
  return {
    selector,
    test(value) {
      return value === getConfirmValue()
        ? undefined
        : message || `Please enter this field`;
    },
  };
};
