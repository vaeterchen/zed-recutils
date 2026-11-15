module.exports = grammar({
  name: "recutils",
  extras: () => [],

  rules: {
    database: $ => seq(
      repeat(choice(seq($._entry, $._newline), $._blank_line)),
      optional($._entry),
    ),

    _entry: $ => choice($.field, $.comment),

    field: $ => seq(
      field("name", choice($.field_name, $.descriptor_name)),
      ":",
      optional(field("value", $.value)),
    ),

    field_name: () => /[A-Za-z][A-Za-z0-9_]*/,
    descriptor_name: () => /%[A-Za-z0-9_]*/,
    comment: () => /#[^\r\n]*/,

    value: $ => repeat1(choice(
      $.value_text,
      $.escaped_newline,
      $.continuation_marker,
    )),

    value_text: () => token(choice(/[^\r\n\\]+/, "\\")),
    escaped_newline: () => token(prec(1, /\\\r?\n/)),
    continuation_marker: () => token(prec(1, /\r?\n\+/)),

    _newline: () => /\r?\n/,
    _blank_line: () => /[ \t]*\r?\n/,
  },
});
