import { Input } from '@/components/ui/input'

export interface ThemeInputProps {
  value: string
  onChange: (value: string) => void
  placeholder?: string
}

export function ThemeInput({ value, onChange, placeholder = 'Theme' }: ThemeInputProps) {
  return (
    <Input value={value} onChange={e => onChange(e.target.value)} placeholder={placeholder} />
  )
}