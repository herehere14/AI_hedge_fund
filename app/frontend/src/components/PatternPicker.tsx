import { Checkbox } from '@/components/ui/checkbox'

const PATTERNS = ['Head and Shoulders', 'Double Bottom', 'Triangle']

export interface PatternPickerProps {
  value: string[]
  onChange: (value: string[]) => void
}

export function PatternPicker({ value, onChange }: PatternPickerProps) {
  const toggle = (pattern: string, checked: boolean) => {
    if (checked) {
      if (!value.includes(pattern)) {
        onChange([...value, pattern])
      }
    } else {
      onChange(value.filter(p => p !== pattern))
    }
  }
  return (
    <div className="space-y-2">
      {PATTERNS.map(p => (
        <label key={p} className="flex items-center gap-2">
          <Checkbox id={p} checked={value.includes(p)} onCheckedChange={c => toggle(p, !!c)} />
          <span>{p}</span>
        </label>
      ))}
    </div>
  )
}