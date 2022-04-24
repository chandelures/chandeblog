from webargs import fields

pagination_args = {
    "page": fields.Int(load_default=1, validate=lambda p: p >= 1),
    "size": fields.Int(load_default=10, validate=lambda s: 1 <= s <= 50)
}
