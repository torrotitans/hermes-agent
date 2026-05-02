---
name: react-hook-form
description: Implement react-hook-form for form management including controlled/uncontrolled inputs, validation, schema validation with Zod/Yup, dynamic fields, and form state management
license: MIT
compatibility:
  - react-18.0+
  - react-hook-form-7.0+
metadata:
  version: 1.0.0
  author: Torro Team
  source: https://www.npmjs.com/package/react-hook-form
---

# React Hook Form Skill

## When to Use This Skill

Use this skill when you need to:
- Create forms with minimal re-renders using react-hook-form
- Implement validation (built-in or schema-based with Zod/Yup)
- Handle dynamic form fields (append, remove, insert)
- Manage form state (watch, setValue, getValues)
- Build controlled components with uncontrolled performance
- Implement file uploads and multi-step forms
- Integrate with UI component libraries (MUI, Chakra, Radix)
- Handle form submission and error states
- Use Controller for third-party input components

## When NOT to Use This Skill

Do NOT use this skill when:
- Building simple static forms without validation (use HTML forms)
- Working with class components (use class-based form libraries)
- Managing global state across the app (use Zustand/Redux)
- Building server-side rendered forms without hydration (use SSR-friendly alternatives)

## Inputs Required

Before starting, ensure you have:
1. React version (default: 18.x+)
2. Form complexity (simple, dynamic, multi-step)
3. Validation requirements (built-in, Zod, Yup)
4. UI component library (if any)

## Workflow

### Step 1: Basic Form Setup

```typescript
import { useForm } from 'react-hook-form'

interface FormData {
  username: string
  email: string
  password: string
}

function BasicForm() {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<FormData>()

  const onSubmit = async (data: FormData) => {
    console.log(data)
    // Submit to API
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register('username', { required: 'Username is required' })} />
      {errors.username && <span>{errors.username.message}</span>}

      <input {...register('email', { required: 'Email is required' })} />
      {errors.email && <span>{errors.email.message}</span>}

      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? 'Submitting...' : 'Submit'}
      </button>
    </form>
  )
}
```

### Step 2: Schema Validation with Zod

```typescript
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'

const schema = z.object({
  username: z.string().min(3, 'Username must be at least 3 characters'),
  email: z.string().email('Invalid email address'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
  age: z.number().min(18, 'Must be 18 or older'),
})

type FormData = z.infer<typeof schema>

function ZodForm() {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<FormData>({
    resolver: zodResolver(schema),
  })

  return (
    <form onSubmit={handleSubmit((data) => console.log(data))}>
      <input {...register('username')} />
      {errors.username && <span>{errors.username.message}</span>}

      <input {...register('email')} />
      {errors.email && <span>{errors.email.message}</span>}

      <input type="number" {...register('age', { valueAsNumber: true })} />
      {errors.age && <span>{errors.age.message}</span>}

      <button type="submit">Submit</button>
    </form>
  )
}
```

### Step 3: Watch and Form State

```typescript
import { useForm } from 'react-hook-form'

function WatchForm() {
  const {
    register,
    watch,
    setValue,
    getValues,
    formState: { errors },
  } = useForm<{
    firstName: string
    lastName: string
    email: string
  }>()

  const firstName = watch('firstName')
  const allValues = watch() // Watch all fields

  const handleReset = () => {
    setValue('firstName', '')
    setValue('lastName', '')
  }

  const getFirstName = () => {
    return getValues('firstName')
  }

  return (
    <form>
      <input {...register('firstName')} />
      <input {...register('lastName')} />
      <input {...register('email')} />

      <p>First name: {firstName}</p>
      <button type="button" onClick={handleReset}>Reset</button>
      <button type="button" onClick={() => console.log(getFirstName())}>
        Get First Name
      </button>
    </form>
  )
}
```

### Step 4: Dynamic Fields (Append/Remove)

```typescript
import { useForm, useFieldArray } from 'react-hook-form'

interface FormData {
  fields: { name: string; value: string }[]
}

function DynamicFieldsForm() {
  const { control, handleSubmit } = useForm<FormData>({
    defaultValues: { fields: [{ name: '', value: '' }] },
  })

  const { fields, append, remove } = useFieldArray({
    control,
    name: 'fields',
  })

  return (
    <form onSubmit={handleSubmit((data) => console.log(data))}>
      {fields.map((field, index) => (
        <div key={field.id}>
          <input
            {...register(`fields.${index}.name`)}
            placeholder="Name"
          />
          <input
            {...register(`fields.${index}.value`)}
            placeholder="Value"
          />
          <button type="button" onClick={() => remove(index)}>
            Remove
          </button>
        </div>
      ))}

      <button type="button" onClick={() => append({ name: '', value: '' })}>
        Add Field
      </button>

      <button type="submit">Submit</button>
    </form>
  )
}
```

### Step 5: Controller for Third-Party Components

```typescript
import { useForm, Controller } from 'react-hook-form'
import { TextField, Select, MenuItem } from '@mui/material'

interface FormData {
  category: string
  description: string
}

function ControllerForm() {
  const { control, handleSubmit } = useForm<FormData>()

  return (
    <form onSubmit={handleSubmit((data) => console.log(data))}>
      <Controller
        name="category"
        control={control}
        render={({ field }) => (
          <Select {...field} placeholder="Select category">
            <MenuItem value="cat1">Category 1</MenuItem>
            <MenuItem value="cat2">Category 2</MenuItem>
          </Select>
        )}
      />

      <Controller
        name="description"
        control={control}
        render={({ field }) => (
          <TextField {...field} multiline rows={4} placeholder="Description" />
        )}
      />

      <button type="submit">Submit</button>
    </form>
  )
}
```

### Step 6: Form with File Upload

```typescript
import { useForm } from 'react-hook-form'

function FileUploadForm() {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<{
    avatar: FileList
    document: FileList
  }>()

  const onSubmit = async (data: { avatar: FileList; document: FileList }) => {
    const formData = new FormData()
    formData.append('avatar', data.avatar[0])
    formData.append('document', data.document[0])

    await fetch('/api/upload', {
      method: 'POST',
      body: formData,
    })
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input
        type="file"
        {...register('avatar', {
          required: 'Avatar is required',
          validate: {
            fileType: (value) =>
              value[0]?.type.startsWith('image/') || 'Must be an image',
            fileSize: (value) =>
              value[0]?.size < 5000000 || 'File must be < 5MB',
          },
        })}
      />
      {errors.avatar && <span>{errors.avatar.message}</span>}

      <input
        type="file"
        {...register('document', { required: 'Document is required' })}
      />
      {errors.document && <span>{errors.document.message}</span>}

      <button type="submit">Upload</button>
    </form>
  )
}
```

### Step 7: Multi-Step Form

```typescript
import { useState } from 'react'
import { useForm } from 'react-hook-form'

interface Step1Data {
  firstName: string
  lastName: string
}

interface Step2Data {
  email: string
  phone: string
}

function MultiStepForm() {
  const [step, setStep] = useState(1)
  const methods = useForm<{ step1: Step1Data; step2: Step2Data }>()

  const onNext = methods.handleSubmit((data) => {
    if (step === 1 && !data.step1.firstName) {
      methods.setError('step1.firstName', { message: 'Required' })
      return
    }
    setStep(step + 1)
  })

  const onBack = () => setStep(step - 1)

  const onSubmit = methods.handleSubmit((data) => {
    console.log('All data:', data)
  })

  return (
    <form>
      {step === 1 && (
        <div>
          <input {...methods.register('step1.firstName')} placeholder="First Name" />
          <input {...methods.register('step1.lastName')} placeholder="Last Name" />
          <button type="button" onClick={onNext}>Next</button>
        </div>
      )}

      {step === 2 && (
        <div>
          <input {...methods.register('step2.email')} placeholder="Email" />
          <input {...methods.register('step2.phone')} placeholder="Phone" />
          <button type="button" onClick={onBack}>Back</button>
          <button type="button" onClick={onSubmit}>Submit</button>
        </div>
      )}
    </form>
  )
}
```

### Step 8: Form with Default Values and Reset

```typescript
import { useForm } from 'react-hook-form'

interface FormData {
  name: string
  email: string
  role: string
}

function EditForm({ initialData }: { initialData: FormData }) {
  const {
    register,
    handleSubmit,
    reset,
    formState: { isDirty },
  } = useForm<FormData>({
    defaultValues: initialData,
  })

  const onSubmit = async (data: FormData) => {
    await fetch('/api/users', {
      method: 'PUT',
      body: JSON.stringify(data),
    })
    reset(data) // Reset dirty state
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register('name')} />
      <input {...register('email')} />
      <input {...register('role')} />

      <button type="submit" disabled={!isDirty}>
        Save
      </button>
      <button type="button" onClick={() => reset(initialData)}>
        Cancel
      </button>
    </form>
  )
}
```

### Step 9: Custom Validation Rules

```typescript
import { useForm } from 'react-hook-form'

function CustomValidationForm() {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<{
    username: string
    password: string
    confirmPassword: string
  }>()

  const onSubmit = (data: any) => console.log(data)

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input
        {...register('username', {
          required: 'Username is required',
          minLength: { value: 3, message: 'Min 3 characters' },
          maxLength: { value: 20, message: 'Max 20 characters' },
          pattern: {
            value: /^[a-zA-Z0-9_]+$/,
            message: 'Only alphanumeric and underscore',
          },
        })}
      />
      {errors.username && <span>{errors.username.message}</span>}

      <input
        type="password"
        {...register('password', {
          required: 'Password is required',
          minLength: { value: 8, message: 'Min 8 characters' },
          validate: {
            hasNumber: (v) => /\d/.test(v) || 'Must contain a number',
            hasUpper: (v) => /[A-Z]/.test(v) || 'Must contain uppercase',
          },
        })}
      />
      {errors.password && <span>{errors.password.message}</span>}

      <input
        {...register('confirmPassword', {
          validate: (value, formValues) =>
            value === formValues.password || 'Passwords do not match',
        })}
      />
      {errors.confirmPassword && <span>{errors.confirmPassword.message}</span>}

      <button type="submit">Submit</button>
    </form>
  )
}
```

### Step 10: Form with Loading and Error States

```typescript
import { useForm } from 'react-hook-form'

function FormWithStates() {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting, submitCount, isValid },
  } = useForm<{ email: string; password: string }>({
    mode: 'onChange', // Validate on change
  })

  const [serverError, setServerError] = useState<string | null>(null)

  const onSubmit = async (data: any) => {
    setServerError(null)
    try {
      await fetch('/api/login', {
        method: 'POST',
        body: JSON.stringify(data),
      })
    } catch (error) {
      setServerError('Login failed. Please try again.')
    }
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register('email', { required: 'Email required' })} />
      {errors.email && <span>{errors.email.message}</span>}

      <input type="password" {...register('password', { required: 'Password required' })} />
      {errors.password && <span>{errors.password.message}</span>}

      {serverError && <div className="error">{serverError}</div>}

      <p>Submit count: {submitCount}</p>
      <p>Form valid: {isValid ? 'Yes' : 'No'}</p>

      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? 'Logging in...' : 'Login'}
      </button>
    </form>
  )
}
```

## Files Reference

| File | Purpose |
|------|---------|
| `src/useForm.ts` | Main useForm hook |
| `src/useFieldArray.ts` | Dynamic fields hook |
| `src/controller.tsx` | Controller component |
| `src/types.ts` | TypeScript types |

## Troubleshooting

### Issue: Form Not Submitting

**Symptom**: `handleSubmit` not triggering

**Solution**:
- Ensure form has `onSubmit={handleSubmit(onSubmitFn)}`
- Check button has `type="submit"`
- Verify no `e.preventDefault()` blocking submission

### Issue: Input Not Updating

**Symptom**: Input value not reflecting state

**Solution**:
- Use `register` for native inputs
- Use `Controller` for third-party components
- Check `defaultValue` vs `value` usage

### Issue: Validation Not Working

**Symptom**: Errors not showing

**Solution**:
- Use `formState: { errors }` destructuring (triggers re-render)
- Check validation rules syntax
- Use `mode: 'onChange'` or `'onSubmit'` in useForm

## Examples

### Example 1: Complete Login Form

```typescript
function LoginForm() {
  const { register, handleSubmit, formState: { errors, isSubmitting } } = useForm<{
    login_name: string
    login_password: string
  }>()

  const onSubmit = async (data) => {
    const response = await fetch('/api/auth/login', {
      method: 'POST',
      body: JSON.stringify(data),
    })
    if (!response.ok) throw new Error('Invalid credentials')
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register('login_name', { required: 'Username required' })} />
      {errors.login_name && <span>{errors.login_name.message}</span>}

      <input type="password" {...register('login_password', { required: 'Password required' })} />
      {errors.login_password && <span>{errors.login_password.message}</span>}

      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? 'Signing in...' : 'Sign in'}
      </button>
    </form>
  )
}
```

### Example 2: Workspace Create Form

```typescript
function WorkspaceCreateForm() {
  const { register, handleSubmit, formState: { errors } } = useForm<{
    name: string
    policyIdPrefix: string
  }>()

  return (
    <form onSubmit={handleSubmit((data) => console.log(data))}>
      <input {...register('name', { required: 'Name required', minLength: 3 })} />
      {errors.name && <span>{errors.name.message}</span>}

      <input {...register('policyIdPrefix', { required: 'Prefix required' })} />
      {errors.policyIdPrefix && <span>{errors.policyIdPrefix.message}</span>}

      <button type="submit">Create Workspace</button>
    </form>
  )
}
```

## Related Resources

- [React Hook Form Documentation](https://react-hook-form.com/)
- [React Hook Form API Reference](https://react-hook-form.com/api/)
- [React Hook Form Examples](https://react-hook-form.com/get-started#CodeExamples)
