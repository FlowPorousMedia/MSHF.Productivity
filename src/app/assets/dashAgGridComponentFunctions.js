var dagcomponentfuncs = window.dashAgGridComponentFunctions = window.dashAgGridComponentFunctions || {};

dagcomponentfuncs.Button = function (props) {
    const { setData } = props;

    function onClick() {
        setData();
    }
    return window.React.createElement(
        'button',
        {
            onClick: onClick,
            className: props.className,
            style: {padding: '5px 10px', fontSize: '12px'}  // Add basic styling
        },
        props.value
    );
};