import { render, screen } from '@testing-library/react';
import Event from './Event';

jest.mock('react-router-dom', () => ({
    useNavigate: () => jest.fn(),
    useSearchParams: () => [new URLSearchParams(), jest.fn()],
}));

test('event description input should be rendered', () => {
    render(<Event />);
    expect(screen.getByTestId('eventDescription')).toBeInTheDocument()
});

test('button addEvent should be rendered', () => {
    render(<Event />);
    expect(screen.getByTestId('buttonAddEvent')).toBeInTheDocument()
});