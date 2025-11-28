export const AdminPublicSchema = {
  type: "object",
  title: "AdminPublic",
  required: ["id", "email", "is_superuser"],
  properties: {
    id: { type: "string", format: "uuid", title: "Id" },
    email: { type: "string", format: "email", maxLength: 255, title: "Email" },
    username: {
      anyOf: [{ type: "string" }, { type: "null" }],
      title: "Username",
    },
    is_superuser: { type: "boolean", title: "Is Superuser" },
  },
} as const;

export const AdminLoginSchema = {
  type: "object",
  title: "AdminLogin",
  required: ["email", "password"],
  properties: {
    email: { type: "string", format: "email", title: "Email" },
    password: {
      type: "string",
      minLength: 8,
      maxLength: 128,
      title: "Password",
    },
  },
} as const;

export const TokenResponseSchema = {
  type: "object",
  title: "TokenResponse",
  required: ["access_token"],
  properties: {
    access_token: { type: "string", title: "Access Token" },
    token_type: { type: "string", title: "Token Type", default: "bearer" },
  },
} as const;

export const TokenPayloadSchema = {
  type: "object",
  title: "TokenPayload",
  properties: {
    sub: { anyOf: [{ type: "string" }, { type: "null" }], title: "Subject" },
  },
} as const;

export const BlogCreateSchema = {
  type: "object",
  title: "BlogCreate",
  required: ["title", "description", "admin_id"],
  properties: {
    title: { type: "string", minLength: 3, maxLength: 100, title: "Title" },
    description: { type: "string", minLength: 5, title: "Description" },
    admin_id: { type: "string", format: "uuid", title: "Admin Id" },
  },
} as const;

export const BlogPublicSchema = {
  type: "object",
  title: "BlogPublic",
  required: [
    "id",
    "title",
    "description",
    "admin_id",
    "created_at",
    "updated_at",
  ],
  properties: {
    id: { type: "string", format: "uuid", title: "Id" },
    title: { type: "string", title: "Title" },
    description: { type: "string", title: "Description" },
    created_at: { type: "string", format: "date-time", title: "Created At" },
    updated_at: { type: "string", format: "date-time", title: "Updated At" },
    admin_id: { type: "string", format: "uuid", title: "Admin Id" },
  },
} as const;

export const BlogsPublicSchema = {
  type: "object",
  title: "BlogsPublic",
  required: ["data", "count"],
  properties: {
    data: {
      type: "array",
      items: { $ref: "#/components/schemas/BlogPublic" },
      title: "Data",
    },
    count: { type: "integer", title: "Count" },
  },
} as const;

export const HTTPValidationErrorSchema = {
  type: "object",
  title: "HTTPValidationError",
  properties: {
    detail: {
      type: "array",
      items: { $ref: "#/components/schemas/ValidationError" },
      title: "Detail",
    },
  },
} as const;

export const ValidationErrorSchema = {
  type: "object",
  title: "ValidationError",
  required: ["loc", "msg", "type"],
  properties: {
    loc: {
      type: "array",
      items: { anyOf: [{ type: "string" }, { type: "integer" }] },
    },
    msg: { type: "string", title: "Message" },
    type: { type: "string", title: "Error Type" },
  },
} as const;
