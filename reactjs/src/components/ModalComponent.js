import Modal from 'react-bootstrap/Modal';
import './ModalComponent.css'

const ModalComponent = (props) => {

    const showModal = props.showModal;
    const label = props.label;

    return (
        <div data-testid="modal">
            <Modal show={showModal} centered>
                <Modal.Body style={{ height: "205px" }}>
                    <div style={{ height: "175px", }} className="center">
                        <span className="loader">{label}</span>
                    </div>
                </Modal.Body>
            </Modal>
        </div>
    );
}

export default ModalComponent;