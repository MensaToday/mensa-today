module.exports = {
  root: true,

  env: {
    node: true,
  },

  extends: [
    "plugin:vue/essential",
    "eslint:recommended",
    "plugin:prettier/recommended",
  ],

  parserOptions: {
    parser: "@babel/eslint-parser",
  },

  rules: {
    "no-console": "off",
    "no-debugger": "off",
    "prettier/prettier": [
      "error",
      {
        "endOfLine": "auto",
      },
    ],
  },
};
