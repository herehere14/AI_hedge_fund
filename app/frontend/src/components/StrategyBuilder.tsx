import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { LegendarySelector } from './LegendarySelector'
import { ThemeInput } from './ThemeInput'
import { PatternPicker } from './PatternPicker'
import { api } from '@/services/api'

export function StrategyBuilder() {
  const [indicator, setIndicator] = useState('')
  const [theme, setTheme] = useState('')
  const [patterns, setPatterns] = useState<string[]>([])
  const [result, setResult] = useState<string>('')

  const handleScan = async () => {
    try {
      const data = await api.scan({ indicator, theme, patterns })
      setResult(JSON.stringify(data))
    } catch (err) {
      setResult('Error running scan')
    }
  }

  const handleBacktest = async () => {
    try {
      const data = await api.backtest({ indicator, theme, patterns })
      setResult(JSON.stringify(data))
    } catch (err) {
      setResult('Error running backtest')
    }
  }

  return (
    <div className="p-4 space-y-4 max-w-md">
      <LegendarySelector value={indicator} onChange={setIndicator} />
      <ThemeInput value={theme} onChange={setTheme} />
      <PatternPicker value={patterns} onChange={setPatterns} />
      <div className="flex gap-2">
        <Button onClick={handleScan}>Scan</Button>
        <Button onClick={handleBacktest}>Backtest</Button>
      </div>
      {result && <pre data-testid="result" className="whitespace-pre-wrap bg-secondary p-2 rounded-md">{result}</pre>}
    </div>
  )
}