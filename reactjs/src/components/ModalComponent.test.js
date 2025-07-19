import { render, screen } from '@testing-library/react';
import ModalComponent from './ModalComponent';

test('modal layout should be rendered', () => {
    render(<ModalComponent />);
    expect(screen.getByTestId('modal')).toBeInTheDocument()
})