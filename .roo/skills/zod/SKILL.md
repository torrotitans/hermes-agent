---
name: zod
description: Implement Zod schema validation including type inference, validation chains, transforms, refinement, and integration with TypeScript for runtime type checking
license: MIT
compatibility:
  - typescript-4.5+
  - zod-3.0+
metadata:
  version: 1.0.0
  author: Torro Team
  source: https://www.npmjs.com/package/zod
---

# Zod Validation Skill

## When to Use This Skill

Use this skill when you need to:
- Define schemas with runtime type validation
- Infer TypeScript types from Zod schemas
- Validate and transform input data (API requests, form data)
- Create nested and recursive schemas
- Implement custom validation rules with refinements
- Use Zod with Zodios, Express, or Fastify for API validation
- Integrate with react-hook-form using @hookform/resolvers
- Create discriminated unions for polymorphic data
- Validate arrays, tuples, and optional fields
- Generate JSON Schema from Zod schemas

## When NOT to Use This Skill

Do NOT use this skill when:
- Building simple static type definitions (use TypeScript interfaces)
- Validating non-TypeScript languages (use language-specific validators)
- Performing complex business logic validation (use domain models)
- Working with legacy JavaScript without TypeScript (use Joi instead)

## Inputs Required

Before starting, ensure you have:
1. TypeScript version (default: 4.5+)
2. Data structure to validate (object, array, union, etc.)
3. Required vs optional fields
4. Custom error messages

## Workflow

### Step 1: Basic Schema Definition

```typescript
import { z } from 'zod'

// String schema
const stringSchema = z.string()
stringSchema.parse('hello') // => 'hello'
stringSchema.parse(123) // => throws ZodError

// Number schema
const numberSchema = z.number()
numberSchema.parse(42) // => 42
numberSchema.parse('42') // => throws ZodError

// Boolean schema
const booleanSchema = z.boolean()
booleanSchema.parse(true) // => true

// Optional and nullable
const optionalString = z.string().optional()
optionalString.parse(undefined) // => undefined
optionalString.parse('hello') // => 'hello'

const nullableString = z.string().nullable()
nullableString.parse(null) // => null
nullableString.parse('hello') // => 'hello'
```

### Step 2: Object Schemas

```typescript
import { z } from 'zod'

const userSchema = z.object({
  id: z.string().uuid(),
  name: z.string().min(2).max(50),
  email: z.string().email(),
  age: z.number().int().positive().optional(),
  role: z.enum(['admin', 'user', 'moderator']).default('user'),
  tags: z.array(z.string()).default([]),
})

type User = z.infer<typeof userSchema>

// Parse and validate
const userData = userSchema.parse({
  id: '550e8400-e29b-41d4-a716-446655440000',
  name: 'John Doe',
  email: 'john@example.com',
  role: 'admin',
})

// Safe parse (returns result instead of throwing)
const result = userSchema.safeParse({
  id: 'invalid-uuid',
  name: 'J',
  email: 'not-an-email',
})

if (!result.success) {
  console.error(result.error.format())
}
```

### Step 3: Type Inference

```typescript
import { z } from 'zod'

const schema = z.object({
  id: z.string(),
  name: z.string(),
  email: z.string().email(),
  age: z.number().optional(),
  isActive: z.boolean().default(true),
})

// Infer TypeScript type
type User = z.infer<typeof schema>
// {
//   id: string
//   name: string
//   email: string
//   age?: number | undefined
//   isActive: boolean
// }

// Infer input type (before transformation)
const transformed = z.string().transform((val) => parseInt(val))
type InputType = z.input<typeof transformed> // string
type OutputType = z.output<typeof transformed> // number
```

### Step 4: String Validations

```typescript
import { z } from 'zod'

const userSchema = z.object({
  username: z
    .string()
    .min(3, { message: 'Username must be at least 3 characters' })
    .max(20, { message: 'Username must be at most 20 characters' })
    .regex(/^[a-zA-Z0-9_]+$/, { message: 'Only alphanumeric and underscores' }),

  email: z
    .string()
    .email({ message: 'Invalid email address' })
    .toLowerCase(),

  password: z
    .string()
    .min(8, { message: 'Password must be at least 8 characters' })
    .regex(/[A-Z]/, { message: 'Must contain uppercase letter' })
    .regex(/[0-9]/, { message: 'Must contain a number' }),

  age: z
    .string()
    .pipe(z.number().min(18).max(120)),

  website: z.string().url().optional().or(z.literal('')),
})
```

### Step 5: Number and Date Validations

```typescript
import { z } from 'zod'

const metricsSchema = z.object({
  score: z.number().min(0).max(100).default(0),
  percentage: z.number().min(0).max(1).describe('Value between 0 and 1'),
  count: z.number().int().positive(),

  birthDate: z.date().max(new Date(), { message: 'Birth date must be in the past' }),
  createdAt: z.date().default(() => new Date()),

  temperature: z.number().describe('Temperature in Celsius'),
})

// Parse from string
const parsed = metricsSchema.parse({
  score: '85', // Will fail - use transform
  count: '5',
})

// With transform
const strictNumber = z.string().transform((val) => {
  const parsed = parseInt(val)
  if (isNaN(parsed)) throw new Error('Invalid number')
  return parsed
})
```

### Step 6: Array and Tuple Validations

```typescript
import { z } from 'zod'

const shoppingListSchema = z.object({
  items: z.array(
    z.object({
      name: z.string(),
      quantity: z.number().int().positive(),
      price: z.number().positive(),
    })
  ).min(1, { message: 'At least one item required' }),

  tags: z.array(z.string()).max(5, { message: 'Maximum 5 tags' }),

  coordinates: z.tuple([
    z.number(), // latitude
    z.number(), // longitude
  ]),

  mixedArray: z.array(z.union([z.string(), z.number()])),

  uniqueTags: z.array(z.string()).refine(
    (tags) => new Set(tags).size === tags.length,
    { message: 'Tags must be unique' }
  ),
})
```

### Step 7: Union and Discriminated Unions

```typescript
import { z } from 'zod'

// Simple union
const stringOrNumber = z.union([z.string(), z.number()])
stringOrNumber.parse('hello') // => 'hello'
stringOrNumber.parse(42) // => 42

// Discriminated union
const messageSchema = z.discriminatedUnion('type', [
  z.object({
    type: 'text',
    content: z.string(),
  }),
  z.object({
    type: 'image',
    url: z.string().url(),
    alt: z.string(),
  }),
  z.object({
    type: 'video',
    url: z.string().url(),
    duration: z.number(),
  }),
])

type Message = z.infer<typeof messageSchema>

// Parse
const textMessage = messageSchema.parse({ type: 'text', content: 'Hello' })
const imageMessage = messageSchema.parse({ type: 'image', url: 'https://example.com/img.jpg', alt: 'Image' })
```

### Step 8: Transforms

```typescript
import { z } from 'zod'

// Basic transform
const trimmedString = z.string().transform((val) => val.trim())

// Parse with transform
const result = trimmedString.parse('  hello  ') // => 'hello'

// Chain transforms
const positiveInt = z
  .string()
  .transform((val) => parseInt(val))
  .transform((val) => (val > 0 ? val : 0))

// Optional with transform
const optionalTransform = z
  .string()
  .optional()
  .transform((val) => val?.toUpperCase())

// Preprocess before validation
const numberWithDefault = z.preprocess(
  (val) => (typeof val === 'string' ? parseFloat(val) : val),
  z.number().min(0)
)
```

### Step 9: Refinements and Custom Validation

```typescript
import { z } from 'zod'

// Simple refinement
const positiveNumber = z.number().refine((num) => num > 0, {
  message: 'Number must be positive',
})

// Refinement with custom error path
const passwordSchema = z.string().refine(
  (val) => val.length >= 8,
  { message: 'Password must be at least 8 characters', path: ['password'] }
)

// Async refinement
const uniqueUsername = z.string().refine(
  async (val) => {
    const response = await fetch(`/api/check-username?username=${val}`)
    const data = await response.json()
    return data.available
  },
  { message: 'Username already taken' }
)

// Custom refinement function
function customRefine<T>(schema: z.ZodType<T>, check: (val: T) => boolean, message: string) {
  return schema.refine(check, { message })
}

const emailSchema = customRefine(
  z.string().email(),
  (val) => !val.endsWith('@spam.com'),
  'Cannot use spam email domains'
)
```

### Step 10: Async Validation

```typescript
import { z } from 'zod'

// Async schema
const asyncSchema = z.object({
  username: z.string().refine(
    async (val) => {
      const response = await fetch(`/api/validate-username?username=${val}`)
      return response.ok
    },
    { message: 'Username unavailable' }
  ),
  email: z.string().email(),
})

// Parse async
async function validateUser(data: unknown) {
  const result = await asyncSchema.safeParseAsync(data)
  if (!result.success) {
    return { error: result.error.format() }
  }
  return { user: result.data }
}

// All errors vs first error
const schema = z.object({
  username: z.string().min(3),
  email: z.string().email(),
  password: z.string().min(8),
})

// First error only
const firstError = schema.safeParse({ username: 'a', email: 'invalid', password: 'short' })
console.log(firstError.error.issues.length) // => 1

// All errors
const allErrors = schema.safeParse({ username: 'a', email: 'invalid', password: 'short' })
console.log(allErrors.error.issues.length) // => 3
```

### Step 11: Integration with react-hook-form

```typescript
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'

const userSchema = z.object({
  name: z.string().min(2, 'Name must be at least 2 characters'),
  email: z.string().email('Invalid email'),
  age: z.number().min(18).optional(),
})

type FormData = z.infer<typeof userSchema>

function UserForm() {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<FormData>({
    resolver: zodResolver(userSchema),
  })

  return (
    <form onSubmit={handleSubmit((data) => console.log(data))}>
      <input {...register('name')} />
      {errors.name && <span>{errors.name.message}</span>}

      <input {...register('email')} />
      {errors.email && <span>{errors.email.message}</span>}

      <input type="number" {...register('age', { valueAsNumber: true })} />
      {errors.age && <span>{errors.age.message}</span>}

      <button type="submit">Submit</button>
    </form>
  )
}
```

### Step 12: Error Formatting

```typescript
import { z } from 'zod'

const schema = z.object({
  username: z.string().min(3),
  email: z.string().email(),
})

const result = schema.safeParse({ username: 'ab', email: 'invalid' })

if (!result.success) {
  // Format as record
  const formatted = result.error.format()
  console.log(formatted.username._errors) // => ['String must contain at least 3 character(s)']
  console.log(formatted.email._errors) // => ['Invalid email']

  // Get flat errors
  const flatErrors = result.error.issues.map((issue) => ({
    field: issue.path.join('.'),
    message: issue.message,
  }))
  // => [{ field: 'username', message: '...' }, { field: 'email', message: '...' }]

  // Get first error message
  const firstError = result.error.errors[0]?.message
}
```

## Files Reference

| File | Purpose |
|------|---------|
| `src/ZodType.ts` | Base type definitions |
| `src/types.ts` | TypeScript type utilities |
| `src/functions.ts` | Validation functions |
| `src/helpers.ts` | Helper utilities |

## Troubleshooting

### Issue: Type Inference Failing

**Symptom**: `z.infer` returns `any`

**Solution**:
- Ensure TypeScript 4.5+ is installed
- Check `strict` mode is enabled in tsconfig
- Use `z.output<T>` or `z.input<T>` for explicit types

### Issue: Validation Not Catching Errors

**Symptom**: Invalid data passes validation

**Solution**:
- Use `.parse()` or `.safeParse()` (not just schema definition)
- Check for `.optional()` or `.default()` allowing undefined
- Verify transform isn't silently converting values

### Issue: Async Validation Not Working

**Symptom**: `safeParseAsync` not available

**Solution**:
- Ensure Zod 3.22+ is installed
- Use `await` with `safeParseAsync()`
- Check refinement is actually async (returns Promise)

## Examples

### Example 1: API Request Validation

```typescript
import { z } from 'zod'

const createUserSchema = z.object({
  body: z.object({
    name: z.string().min(2).max(50),
    email: z.string().email(),
    password: z.string().min(8),
    role: z.enum(['admin', 'user']).default('user'),
  }),
})

type CreateUserRequest = z.infer<typeof createUserSchema>['body']

async function handleCreateUser(request: Request) {
  const body = await request.json()
  const result = createUserSchema.safeParse({ body })

  if (!result.success) {
    return new Response(
      JSON.stringify({ error: result.error.format() }),
      { status: 400 }
    )
  }

  // Create user with result.data.body
  return new Response(JSON.stringify({ success: true }), { status: 201 })
}
```

### Example 2: Configuration Schema

```typescript
import { z } from 'zod'

const configSchema = z.object({
  port: z.number().int().min(1).max(65535).default(3000),
  host: z.string().default('localhost'),
  database: z.object({
    url: z.string().url(),
    poolSize: z.number().int().min(1).default(10),
  }),
  redis: z.object({
    url: z.string().url().optional(),
    ttl: z.number().int().positive().default(3600),
  }).optional(),
  logging: z.object({
    level: z.enum(['debug', 'info', 'warn', 'error']).default('info'),
    format: z.enum(['json', 'text']).default('json'),
  }),
})

type Config = z.infer<typeof configSchema>
```

## Related Resources

- [Zod Documentation](https://zod.dev/)
- [Zod API Reference](https://zod.dev/manual/v3/basic-usage)
- [Zod to TypeScript](https://zod.dev/COMPATIBILITY#typescript)
