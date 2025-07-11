import { render, fireEvent } from '@testing-library/react'
import { PatternPicker } from '../PatternPicker'

describe('PatternPicker', () => {
  it('toggles pattern', () => {
    const handle = vi.fn()
    const { getByLabelText } = render(<PatternPicker value={[]} onChange={handle} />)
    fireEvent.click(getByLabelText('Head and Shoulders'))
    expect(handle).toHaveBeenCalledWith(['Head and Shoulders'])
  })
})