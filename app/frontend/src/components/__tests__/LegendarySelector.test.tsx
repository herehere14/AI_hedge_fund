import { render, fireEvent } from '@testing-library/react'
import { LegendarySelector } from '../LegendarySelector'

describe('LegendarySelector', () => {
  it('calls onChange when option selected', () => {
    const handle = vi.fn()
    const { getByRole, getByText } = render(<LegendarySelector value="" onChange={handle} />)
    fireEvent.click(getByRole('button'))
    fireEvent.click(getByText('RSI'))
    expect(handle).toHaveBeenCalledWith('RSI')
  })
})