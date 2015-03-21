r"""
Associated Graded Algebras To Filtered Algebras

AUTHORS:

- Travis Scrimshaw (2014-10-08): Initial version
"""

#*****************************************************************************
#  Copyright (C) 2014 Travis Scrimshaw <tscrim at ucdavis.edu>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#                  http://www.gnu.org/licenses/
#*****************************************************************************

from sage.misc.cachefunc import cached_method
from copy import copy

from sage.categories.algebras_with_basis import AlgebrasWithBasis
from sage.sets.family import Family
from sage.combinat.free_module import CombinatorialFreeModule

class AssociatedGradedAlgebra(CombinatorialFreeModule):
    r"""
    The associated graded algebra `\operatorname{gr} A`
    of a filtered algebra with basis `A`.

    Let `A` be a filtered algebra over a commutative ring `R`.
    Let `(F_i)_{i \in I}` be the filtration of `A`, with `I` being
    a totally ordered set. Define

    .. MATH::

        G_i = F_i / \sum_{j < i} F_j

    for every `i \in I`, and then

    .. MATH::

        \operatorname{gr} A = \bigoplus_{i \in I} G_i.

    There are canonical projections `p_i : F_i \to G_i` for
    every `i \in I`. Moreover `\operatorname{gr} A` is naturally a
    graded `R`-module with `G_i` being the `i`-th graded component.

    Let `u \in G_i` and `v \in G_j`, and let `u' \in F_i` and
    `v' \in F_j` be lifts of `u` and `v`, respectively (so that
    `u = p_i(u')` and `v = p_j(v')`). Then, we define a
    multiplication `*` on `\operatorname{gr} A` (not to be mistaken
    for the multiplication of the original algebra `A`) by

    .. MATH::

        u * v = p_{i+j} (u' v').

    The *associated graded algebra* (or, for short, just
    *graded algebra*) of `A` is the graded algebra
    `\operatorname{gr} A` (endowed with this multiplication).

    Now, assume that `A` is a filtered `R`-algebra with basis.
    Let `(b_x)_{x \in X}` be the basis of `A`,
    and consider the partition `X = \bigsqcup_{i \in I} X_i` of
    the set `X`, which is part of the data of a filtered
    algebra with basis. We know (see
    :class:`~sage.categories.filtered_modules_with_basis.FilteredModulesWithBasis`)
    that `A` (being a filtered `R`-module with basis) is canonically
    (when the basis is considered to be part of the data)
    isomorphic to `\operatorname{gr} A` as an `R`-module. Therefore
    the `k`-th graded component `G_k` can be identified with
    the span of `(b_x)_{x \in X_k}`, or equivalently the
    `k`-th homogeneous component of `A`. Suppose
    that `u' v' = \sum_{k \leq i+j} m_k` where `m_k \in G_k` (which
    has been identified with the `k`-th homogeneous component of `A`).
    Then `u * v = m_{i+j}`. We also note that the choice of
    identification of `G_k` with the `k`-th homogeneous component
    of `A` depends on the given basis.

    The basis `(b_x)_{x \in X}` of `A` gives rise to a basis
    of `\operatorname{gr} A`. This latter basis is still indexed
    by the elements of `X`, and consists of the images of the
    `b_x` under the `R`-module isomorphism from `A` to
    `\operatorname{gr} A`. It makes `\operatorname{gr} A` into
    a graded `R`-algebra with basis.

    In this class, the `R`-module isomorphism from `A` to
    `\operatorname{gr} A` is implemented as
    :meth:`to_graded_conversion` and also as the default
    conversion from `A` to `\operatorname{gr} A`. Its
    inverse map is implemented as
    :meth:`from_graded_conversion`.
    The projection `p_i : F_i \to G_i` is implemented as
    :meth:`projection` ``(i)``.

    INPUT:

    - ``A`` -- a filtered algebra with basis

    EXAMPLES::

        sage: A = Algebras(QQ).WithBasis().Filtered().example()
        sage: grA = A.graded_algebra()
        sage: grA.category()
        Category of graded algebras with basis over Rational Field
        sage: x,y,z = map(lambda s: grA.algebra_generators()[s], ['x','y','z'])
        sage: x
        bar(U['x'])
        sage: y * x + z
        bar(U['x']*U['y']) + bar(U['z'])
        sage: A(y) * A(x) + A(z)
        U['x']*U['y']

    We note that the conversion between ``A`` and ``grA`` is
    the canonical ``QQ``-module isomorphism stemming from the
    fact that the underlying ``QQ``-modules of ``A`` and
    ``grA`` are isomorphic::

        sage: grA(A.an_element())
        bar(U['x']^2*U['y']^2*U['z']^3)
        sage: elt = A.an_element() + A.algebra_generators()['x'] + 2
        sage: grelt = grA(elt); grelt
        bar(U['x']^2*U['y']^2*U['z']^3) + bar(U['x']) + 2*bar(1)
        sage: A(grelt) == elt
        True

    .. TODO::

        The algebra ``A`` must currently be an instance of (a subclass of)
        :class:`CombinatorialFreeModule`. This should work with any
        filtered algebra with a basis.

    .. TODO::

        Implement a version of associated graded algebra for
        filtered algebras without a distinguished basis.

    REFERENCES:

    - :wikipedia:`Filtered_algebra#Associated_graded_algebra`
    """
    def __init__(self, A, category=None):
        """
        Initialize ``self``.

        EXAMPLES::

            sage: A = Algebras(QQ).WithBasis().Filtered().example()
            sage: grA = A.graded_algebra()
            sage: TestSuite(grA).run(elements=[prod(grA.algebra_generators())])
        """
        if A not in AlgebrasWithBasis(A.base_ring().category()).Filtered():
            raise ValueError("the base algebra must be filtered and with basis")
        self._A = A

        base_ring = A.base_ring()
        base_one = base_ring.one()

        if category is None:
            category = A.category().Graded()
        opts = copy(A.print_options())
        if not opts['prefix'] and not opts['bracket']:
            opts['bracket'] = '('
        opts['prefix'] = opts['prefix'] + 'bar'

        CombinatorialFreeModule.__init__(self, base_ring, A.indices(),
                                         category=category, **opts)

        # Setup the conversion back
        phi = self.module_morphism(diagonal=lambda x: base_one, codomain=A)
        self._A.register_conversion(phi)

    def _repr_(self):
        """
        Return a string representation of ``self``.

        EXAMPLES::

            sage: A = Algebras(QQ).WithBasis().Filtered().example()
            sage: A.graded_algebra()
            Graded Algebra of An example of a filtered algebra with basis:
             the universal enveloping algebra of Lie algebra of RR^3
             with cross product over Rational Field
        """
        return "Graded Algebra of {}".format(self._A)

    def _latex_(self):
        r"""
        Return a latex representation of ``self``.

        EXAMPLES::

            sage: A = Algebras(QQ).WithBasis().Filtered().example()
            sage: latex(A.graded_algebra())
            \operatorname{gr} ...
        """
        from sage.misc.latex import latex
        return "\\operatorname{gr} " + latex(self._A)

    def _element_constructor_(self, x):
        r"""
        Construct an element of ``self`` from ``x``.

        If ``self`` `= \operatorname{gr} A` for a filtered algebra
        `A` with basis, and if ``x`` is an element of `A`, then
        this returns the image of `x` under the canonical `R`-module
        isomorphism `A \to \operatorname{gr} A`. (In this case,
        this is equivalent to calling
        ``self.to_graded_conversion()(x)``.)

        EXAMPLES::

            sage: A = Algebras(QQ).WithBasis().Filtered().example()
            sage: grA = A.graded_algebra()
            sage: grA(A.an_element())
            bar(U['x']^2*U['y']^2*U['z']^3)
            sage: grA(A.an_element() + A.algebra_generators()['x'] + 2)
            bar(U['x']^2*U['y']^2*U['z']^3) + bar(U['x']) + 2*bar(1)
        """
        if isinstance(x, CombinatorialFreeModule.Element):
            if x.parent() is self._A:
                return self._from_dict(dict(x))
        return super(AssociatedGradedAlgebra, self)._element_constructor_(x)

    def gen(self, *args, **kwds):
        """
        Return a generator of ``self``.

        EXAMPLES::

            sage: A = Algebras(QQ).WithBasis().Filtered().example()
            sage: grA = A.graded_algebra()
            sage: grA.gen('x')
            bar(U['x'])
        """
        try:
            x = self._A.gen(*args, **kwds)
        except AttributeError:
            x = self._A.algebra_generators()[args[0]]
        return self(x)

    @cached_method
    def algebra_generators(self):
        """
        Return the algebra generators of ``self``.

        This assumes that the algebra generators of `A` provided by
        its ``algebra_generators`` method are homogeneous.

        EXAMPLES::

            sage: A = Algebras(QQ).WithBasis().Filtered().example()
            sage: grA = A.graded_algebra()
            sage: grA.algebra_generators()
            Finite family {'y': bar(U['y']), 'x': bar(U['x']), 'z': bar(U['z'])}
        """
        G = self._A.algebra_generators()
        return Family(G.keys(), lambda x: self(G[x]), name="generator")

    def degree_on_basis(self, x):
        """
        Return the degree of the basis element indexed by ``x``.

        EXAMPLES::

            sage: A = Algebras(QQ).WithBasis().Filtered().example()
            sage: grA = A.graded_algebra()
            sage: all(A.degree_on_basis(x) == grA.degree_on_basis(x)
            ....:     for g in grA.algebra_generators() for x in g.support())
            True
        """
        return self._A.degree_on_basis(x)

    @cached_method
    def one_basis(self):
        """
        Return the basis index of the element `1` of
        `\operatorname{gr} A`.

        This assumes that the unity `1` of `A` belongs to `F_0`.

        EXAMPLES::

            sage: A = Algebras(QQ).WithBasis().Filtered().example()
            sage: grA = A.graded_algebra()
            sage: grA.one_basis()
            1
        """
        return self._A.one_basis()

    def product_on_basis(self, x, y):
        """
        Return the product on basis elements given by the
        indices ``x`` and ``y``.

        EXAMPLES::

            sage: A = Algebras(QQ).WithBasis().Filtered().example()
            sage: grA = A.graded_algebra()
            sage: G = grA.algebra_generators()
            sage: x,y,z = G['x'], G['y'], G['z']
            sage: x * y # indirect doctest
            bar(U['x']*U['y'])
            sage: y * x
            bar(U['x']*U['y'])
            sage: z * y * x
            bar(U['x']*U['y']*U['z'])
        """
        ret = self._A.product_on_basis(x, y)
        deg = self._A.degree_on_basis(x) + self._A.degree_on_basis(y)
        return self.sum_of_terms([(i,c) for i,c in ret
                                     if self._A.degree_on_basis(i) == deg],
                                 distinct=True)

