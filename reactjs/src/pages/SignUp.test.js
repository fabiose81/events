import { render, screen, fireEvent } from '@testing-library/react';
import SignUp from './SignUp';

jest.mock('react-router-dom', () => ({
    useNavigate: () => jest.fn(),
    useSearchParams: () => [new URLSearchParams(), jest.fn()],
}));

test('username input should be rendered', () => {
    render(<SignUp />);
    expect(screen.getByTestId('email')).toBeInTheDocument()
});

test('password input should be rendered', () => {
    render(<SignUp />);
    expect(screen.getByTestId('password')).toBeInTheDocument()
});

test('repeat password should be rendered', () => {
    render(<SignUp />);
    expect(screen.getByTestId('repassword')).toBeInTheDocument()
});

test('button save should be rendered', () => {
    render(<SignUp />);
    expect(screen.getByTestId('buttonSave')).toBeInTheDocument()
});

test('username input should changed', () => {
    render(<SignUp />);
    const usernameInputEl = screen.getByTestId('email');
    const email = 'user@email.com';

    fireEvent.change(usernameInputEl, { target: { value: email}});
    expect(usernameInputEl.value).toBe(email);
});

test('password input should changed', () => {
    render(<SignUp />);
    const passwordInputEl = screen.getByTestId('password');
    const password = '123456';

    fireEvent.change(passwordInputEl, { target: { value: password}});
    expect(passwordInputEl.value).toBe(password);
});

test('repassword input should changed', () => {
    render(<SignUp />);
    const passwordInputEl = screen.getByTestId('repassword');
    const password = '123456';

    fireEvent.change(passwordInputEl, { target: { value: password}});
    expect(passwordInputEl.value).toBe(password);
});

test('button save should be disabled', () => {
    render(<SignUp />);
    expect(screen.getByTestId('buttonSave')).toBeDisabled()
});

test('button save should be disabled when email not match', () => {
    render(<SignUp />);
    const usernameInputEl = screen.getByTestId('email');
    const email = 'user@email';
    fireEvent.change(usernameInputEl, { target: { value: email}});

    const passwordInputEl = screen.getByTestId('password');
    const password = '123456';
    fireEvent.change(passwordInputEl, { target: { value: password}});
    expect(screen.getByTestId('buttonSave')).toBeDisabled()
});

test('button save should be enabled', () => {
    render(<SignUp />);
    const usernameInputEl = screen.getByTestId('email');
    const email = 'user@email.com';
    fireEvent.change(usernameInputEl, { target: { value: email}});

    const passwordInputEl = screen.getByTestId('password');
    const password = 'Teste11!';
    fireEvent.change(passwordInputEl, { target: { value: password}});

    const repasswordInputEl = screen.getByTestId('repassword');
    const repassword = 'Teste11!';
    fireEvent.change(repasswordInputEl, { target: { value: repassword}});

    expect(screen.getByTestId('buttonSave')).not.toBeDisabled()
});