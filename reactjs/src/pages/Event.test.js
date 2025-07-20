import { render, screen, fireEvent } from '@testing-library/react';
import Event from './Event';

jest.mock('react-router-dom', () => ({
    useNavigate: () => jest.fn(),
    useSearchParams: () => [new URLSearchParams(), jest.fn()],
}));

afterEach(() => {
    jest.resetAllMocks();
});

test('event description input should be rendered', () => {
    render(<Event />);
    expect(screen.getByTestId('eventDescription')).toBeInTheDocument()
});

test('button addEvent should be rendered', () => {
    render(<Event />);
    expect(screen.getByTestId('buttonAddEvent')).toBeInTheDocument()
});

test('username input should changed', () => {
    render(<Event />);
    const eventDescription = screen.getByTestId('eventDescription');
    const event = 'go to gym';

    fireEvent.change(eventDescription, { target: { value: event}});
    expect(eventDescription.value).toBe(event);
});