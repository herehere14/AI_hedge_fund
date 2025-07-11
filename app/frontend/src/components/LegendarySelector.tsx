import { ChevronsUpDown } from 'lucide-react'
import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Command, CommandGroup, CommandInput, CommandItem, CommandList } from '@/components/ui/command'
import { Popover, PopoverContent, PopoverTrigger } from '@/components/ui/popover'

const OPTIONS = ['RSI', 'MACD', 'Moving Average', 'Bollinger Bands']

export interface LegendarySelectorProps {
  value: string
  onChange: (value: string) => void
}

export function LegendarySelector({ value, onChange }: LegendarySelectorProps) {
  const [open, setOpen] = useState(false)

  return (
    <Popover open={open} onOpenChange={setOpen}>
      <PopoverTrigger asChild>
        <Button variant="outline" role="combobox" className="w-full justify-between">
          {value || 'Select indicator'}
          <ChevronsUpDown className="h-4 w-4 opacity-50" />
        </Button>
      </PopoverTrigger>
      <PopoverContent className="p-0">
        <Command>
          <CommandInput placeholder="Search" className="h-9" />
          <CommandList>
            <CommandGroup>
              {OPTIONS.map(option => (
                <CommandItem key={option} onSelect={() => { onChange(option); setOpen(false) }} className="cursor-pointer">
                  {option}
                </CommandItem>
              ))}
            </CommandGroup>
          </CommandList>
        </Command>
      </PopoverContent>
    </Popover>
  )
}
