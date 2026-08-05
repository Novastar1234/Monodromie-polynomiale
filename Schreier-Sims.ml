(* for permutations p1 and p2, p1 p2 is p1 then p2 
    we suppose that for a generating set g_ = [g1,...,gm], g_ contains the inverse of each of its element
    *)

type perm = {n:int;eval:int array}
let identity n=
    {n=n;eval =Array.init n (fun i-> i)}
let inverse_perm sigma=
    let n =sigma.n in
    let get_antecedent x=
        let rec get_antecedent_aux x k=
            if k>=n then
                failwith "x not in Im(sigma)"
            else
                if sigma.eval.(k) =x then k else get_antecedent_aux x (k+1) in
        get_antecedent_aux x 0 in
    {n=n;eval=Array.init n get_antecedent};;
let compose p1 p2=(*applying p1 then p2*)    
    let n =p1.n in 
    {n=n;eval=Array.init n (fun i->p2.eval.(p1.eval.(i)))};;
let add_inverses g_ = 
    let rec aux reste = match reste with 
                        |[]->[]
                        |g::tl->g::(inverse_perm g)::aux tl in 
    aux g_;;
let get_pointnonfixe g =
    let n =g.n in
    let rec aux k=
        if k>=n then -1
        else 
            if g.eval.(k)=k then aux (k+1)
            else k in
    aux 0;;


type sub_set={n:int;is_in:bool array}
let empty n = 
    {n=n;is_in=Array.make n false};;
let add subset k =
    subset.is_in.(k)<-true;;
let sub_set_size sub_set=
    let count = ref 0 in
    for i =0 to (sub_set.n-1) do
        if sub_set.is_in.(i) then count:= 1+ !count
        done;
    !count


type schreier_vector={n:int;transition:perm array} (*we store inverses*)
let init_scheier_vector n=
    {n=n;transition=Array.make n (identity n)};;
let get_representative delta vector w invert= 
    let rec aux gamma r=
        if gamma = w then if invert then r else inverse_perm r
        else let g_inverse = vector.transition.(gamma) in aux (g_inverse.eval.(gamma)) (compose r g_inverse) in
    aux delta (identity vector.n);;


type chain_link= TRIVIAL
                |Link of {
                    mutable generator: perm list;
                    w : int;
                    orbit:sub_set;
                    mutable stabilizer:chain_link;
                    transversal: schreier_vector
                }
let rec element_test (c : chain_link) (g : perm) : bool=
    match c with
    |TRIVIAL -> g=(identity (g.n))
    |Link(link) -> let delta= g.eval.(link.w) in 
                    link.orbit.is_in.(delta) && 
                    (let r = get_representative delta link.transversal link.w true in 
                        element_test link.stabilizer (compose g r));;
let schreir_sims (g_:perm list):chain_link = (*<g_>=G*)
    let rec extend (c:chain_link) (g:perm):chain_link =
        if element_test c g then c
        else 
            let g_inverse = inverse_perm g in
            match c with
            |TRIVIAL-> begin
                        let w = get_pointnonfixe g in
                        let o =empty g.n in add o w;
                        let t = init_scheier_vector g.n in 

                        let rec get_orbit  delta =
                            let gamma = g.eval.(delta) in
                            if gamma = w then  ()
                            else (add o gamma;t.transition.(gamma)<-g_inverse;get_orbit gamma) in
                        get_orbit w;
                        Link({generator = [g];w=w;orbit=o;stabilizer=(extend TRIVIAL g);transversal=t})
                        end
            |Link(link)->   begin
                            link.generator <- (g::link.generator);
                            let newelements = ref [] in
 
                            let  traiter a a_inverse i =
                                let gamma = a.eval.(i) in
                                    if link.orbit.is_in.(gamma) then
                                        let s = compose (get_representative i link.transversal link.w false) (compose a (get_representative gamma link.transversal link.w true)) in
                                        link.stabilizer <- (extend link.stabilizer s) 
                                    else
                                        ( add link.orbit gamma; newelements := gamma::(!newelements);link.transversal.transition.(gamma)<-(inverse_perm a)) in

                            let traiter_el i=
                                let rec aux reste =
                                    match reste with 
                                    |[]->()
                                    |a::tl->(traiter a (inverse_perm a) i;aux tl) in
                                    aux link.generator in


                            for i = 0 to (g.n -1) do
                                if link.orbit.is_in.(i) then 
                                    traiter g g_inverse i
                                done;
                                
                            let rec traiter_nouveaux ()=
                                match !newelements with
                                |[]->()
                                |i::tl->(newelements := tl;traiter_el i;traiter_nouveaux ()) in
                            traiter_nouveaux ();
                            Link(link)
                            end in

    let rec aux (reste:perm list) (c:chain_link):chain_link=
        match reste with
        |[]->c
        |g::tl-> aux tl (extend c g) in
    aux g_ TRIVIAL;;




let rec chain_link_size (c:chain_link):int = (*we suppose it is proper*)
    match c with |TRIVIAL->1 |Link(link)->(sub_set_size link.orbit) * (chain_link_size link.stabilizer)

let rec factorial n =if n<2 then 1 else n*(factorial (n-1));;
let est_generateur (n:int) (g_:perm list)= (*on suppose que g_ contient inverses*)
    factorial n = chain_link_size (schreir_sims g_);;
