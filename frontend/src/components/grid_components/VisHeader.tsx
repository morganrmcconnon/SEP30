import arrowAll from "../../assets/arrow-all.svg";
// import dotsVertical from "../../assets/dots-vertical.svg";

const VisHeader = ({ title, subtitle }: { title: string, subtitle: string }) => {

    return (
        <div className="vis-header">
            <div className="vis-drag-handle">
                <img src={arrowAll} />
            </div>
            <div className="vis-header-title">
                <h3>{title}</h3>
                <p className="text-subtitle">{subtitle}</p>
            </div>
            {/* <img className="vis-dots" src={dotsVertical} /> */}
        </div>
    );
};

export default VisHeader;