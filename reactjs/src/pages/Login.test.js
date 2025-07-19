import { render, screen, fireEvent } from '@testing-library/react';
import Login from './Login';

jest.mock('react-router-dom', () => ({
    useNavigate: () => jest.fn(),
    useSearchParams: () => [new URLSearchParams(), jest.fn()],
}));

beforeAll(() => {
    process.env.REACT_APP_API_URL = 'http://localhost:8080/'
});

afterEach(() => {
    jest.resetAllMocks();
});

test('username input should be rendered', () => {
    render(<Login />);
    expect(screen.getByTestId('email')).toBeInTheDocument()
});

test('password input should be rendered', () => {
    render(<Login />);
    expect(screen.getByTestId('password')).toBeInTheDocument()
});

test('button login should be rendered', () => {
    render(<Login />);
    expect(screen.getByTestId('buttonLogin')).toBeInTheDocument()
});

test('button sing-up should be rendered', () => {
    render(<Login />);
    expect(screen.getByTestId('signUp')).toBeInTheDocument()
});

test('username input should changed', () => {
    render(<Login />);
    const usernameInputEl = screen.getByTestId('email');
    const email = 'user@email.com';

    fireEvent.change(usernameInputEl, { target: { value: email}});
    expect(usernameInputEl.value).toBe(email);
});

test('password input should changed', () => {
    render(<Login />);
    const passwordInputEl = screen.getByTestId('password');
    const password = '123456';

    fireEvent.change(passwordInputEl, { target: { value: password}});
    expect(passwordInputEl.value).toBe(password);
});

test('button login should be disabled', () => {
    render(<Login />);
    expect(screen.getByTestId('buttonLogin')).toBeDisabled()
});

test('button login should be disabled when email not match', () => {
    render(<Login />);
    const usernameInputEl = screen.getByTestId('email');
    const email = 'user@email';
    fireEvent.change(usernameInputEl, { target: { value: email}});

    const passwordInputEl = screen.getByTestId('password');
    const password = '123456';
    fireEvent.change(passwordInputEl, { target: { value: password}});
    expect(screen.getByTestId('buttonLogin')).toBeDisabled()
});

test('button login should be enabled', () => {
    render(<Login />);
    const usernameInputEl = screen.getByTestId('email');
    const email = 'user@email.com';
    fireEvent.change(usernameInputEl, { target: { value: email}});

    const passwordInputEl = screen.getByTestId('password');
    const password = '123456';
    fireEvent.change(passwordInputEl, { target: { value: password}});

    expect(screen.getByTestId('buttonLogin')).not.toBeDisabled()
});