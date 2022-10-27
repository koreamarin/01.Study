var Body = {
    setColor : function (color) {
        // document.querySelector('body').style.color = color;
        $('body').css('color',color)
    },
    setbackgroundColor : function (color) {
        // document.querySelector('body').style.backgroundColor = color;
        $('body').css('backgroundColor',color)
    }
}

var Links = {
    setColor : function (color) {
        // var a_elements = document.querySelectorAll('a');
        // var i = 0;
        // while(i < a_elements.length) {
        //     a_elements[i].style.color=color;
        //     i+=1;
        // }
        $('a').css('color',color);
    }
}

function nightDayHandler(self) {
    if (self.value === 'day') {
        Body.setbackgroundColor('white');
        Body.setColor('black');
        self.value = 'night';
        Links.setColor('blue');
    }
    else {
        Body.setbackgroundColor('black');
        Body.setColor('white');
        self.value = 'day';
        Links.setColor('powderblue');
    }
}

function sum(number1, number2) {
    return (parseInt(number1) + parseInt(number2));
}