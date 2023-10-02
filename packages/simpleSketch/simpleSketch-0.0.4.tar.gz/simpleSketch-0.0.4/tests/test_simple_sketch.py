#  TODO:

from simple_sketch import SimpleSketch


# simple_sketch.while_lang.syntax/while_lang.lark
#from importlib.resources import files
# files('simple_sketch.while_lang.syntax').joinpath('while_lang.lark').read_text()
if __name__ == "__main__":
    
    SimpleSketch(max_itr_num=100).synthesize(
        # FIXME: Get the correct counterexample for this kind of program
        # XXX: `Counterexample:[x = 15, div0 = [else -> 0], mod0 = [else -> 0]]`
        program=r""" 
            bool b := True; 
            int x := x0;
            while (b) { 
                if (x <= 5) {b := ?? == 1;}
                x := x - 1; 
            }
            assert (not(b) == False);
        """,
        input_output_examples=[
            ('And(x0 == 10)', 'And( x == 5)', '')
            # (('And(x == 15)','{ x : float}'), ('And( x == 3)', '{ x : float}')),
            # (('And(a == 5, b == 2)',''), ('sum == 10', '')),
        ],
        pre_condition = 'True',
        post_condition = 'True',
        loop_inv=""
    )

    SimpleSketch(max_itr_num=100).synthesize(
        # FIXME: Get the correct counterexample for this kind of program
        # XXX: `Counterexample:[x = 15, div0 = [else -> 0], mod0 = [else -> 0]]`
        program=r""" 
            b := b0;
            i := 0 ;
            while (i < n) { 
                b := b + x ; 
                i := i + 1 ;
            }
        """,
        input_output_examples=[
        ],
        pre_condition = 'And(n >=0, b0 >= 0, x>=0)',
        post_condition = 'And(b == b0 + n * x, i ==n)',
        loop_inv= 'And( i <= n, b == x*i + b0)'
    )

    SimpleSketch(max_itr_num=100).synthesize(
        # FIXME: Get the correct counterexample for this kind of program
        # XXX: `Counterexample:[x = 15, div0 = [else -> 0], mod0 = [else -> 0]]`
        program=r""" 
            assume ( n == 5);
            assume ( b0 == 2);
            b := b0;
            i := 0 ;
            x := ??;
            while (i < n) { 
                b := b + x ; 
                i := i + 1 ;
            }
            assert ( b == 2 + 3*5);
        """,
        input_output_examples=[
        ],
        pre_condition = 'And(n >=0, b0 >= 0, x>=0)',
        post_condition = 'And(b == b0 + n * x, i ==n)',
        loop_inv= 'And( i <= n, b == x*i + b0)'
    )
