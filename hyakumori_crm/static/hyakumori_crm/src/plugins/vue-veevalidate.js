import * as rules from "vee-validate/dist/rules";

import { configure, extend } from "vee-validate";

const setupVeeValidate = i18n => {
  Object.keys(rules).forEach(rule => {
    extend(rule, rules[rule]);
  });

  configure({
    defaultMessage: (field, values) => {
      values._field_ = i18n.t(`${field}`);
      return i18n.t(`validations.${values._rule_}`, values);
    },
  });
};

export default setupVeeValidate;
