import { render, fireEvent, waitFor } from '@testing-library/react'
import { StrategyBuilder } from '../StrategyBuilder'
import { vi } from 'vitest'

vi.mock('../../services/api', () => ({
  api: {
    scan: vi.fn(async () => ({ ok: true })),
    backtest: vi.fn(async () => ({ ok: true }))
  }
}))

describe('StrategyBuilder', () => {
  it('calls scan', async () => {
    const { getByText } = render(<StrategyBuilder />)
    fireEvent.click(getByText('Scan'))
    await waitFor(() => {
      expect(require('../../services/api').api.scan).toHaveBeenCalled()
    })
  })

  it('calls backtest', async () => {
    const { getByText } = render(<StrategyBuilder />)
    fireEvent.click(getByText('Backtest'))
    await waitFor(() => {
      expect(require('../../services/api').api.backtest).toHaveBeenCalled()
    })
  })
})