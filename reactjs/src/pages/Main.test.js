import { render, screen } from '@testing-library/react';
import Main from './Main';

jest.mock('react-router-dom', () => ({
    useNavigate: () => jest.fn(),
    useSearchParams: () => [new URLSearchParams(), jest.fn()],
}));

test('navbar should be rendered', () => {
    render(<Main />);
    expect(screen.getByTestId('navbar')).toBeInTheDocument()
});
