import { render, fireEvent } from '@testing-library/react'
import { ThemeInput } from '../ThemeInput'

describe('ThemeInput', () => {
  it('updates value', () => {
    const handle = vi.fn()
    const { getByPlaceholderText } = render(<ThemeInput value="" onChange={handle} />)
    fireEvent.change(getByPlaceholderText('Theme'), { target: { value: 'Tech' } })
    expect(handle).toHaveBeenCalledWith('Tech')
  })
})