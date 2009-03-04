#!/usr/bin/perl

package Perceptron;

use strict;
use warnings;

sub new {
    my ($class, $size) = @_;
    my @weight = ();
    $size += 1;
    for (my $i = 0; $i < $size; $i++) {
        push @weight, 0;
    }
    my $self = {
        weight => \@weight,
        size   => $size,
    };
    bless $self, $class;
    return $self;
}

sub train {
    my ($self, $traindata, $niter) = @_;
    return if !$traindata || $niter < 1;
    for (my $i = 0; $i < $niter; $i++) {
        foreach my $data (@{ $traindata }) {
            $self->_train($data->{data}, $data->{pn});
        }
    }
}

sub _train {
    my ($self, $input, $pn) = @_;
    return if !$input;
    my @data = (1);
    foreach my $x (@{ $input }) {
        push @data, $x;
    }
    my $prod = _product($self->{weight}, \@data);
    if (_sign($prod) != $pn) {
        if ($pn == -1) {
            map { $data[$_] *= $pn } (0 .. scalar(@data)-1);
        }
        $self->_update_weight(\@data);
    }
}

sub predict {
    my ($self, $input) = @_;
    my @data = (1);
    foreach my $x (@{ $input }) {
        push @data, $x;
    }
    my $prod = _product($self->{weight}, \@data);
    return $prod > 0 ? 1 : 0;
}

sub _update_weight {
    my ($self, $data) = @_;
    return if !$data;
    my $size = scalar(@{ $data });
    $size = $self->{size} if $size > $self->{size};
    for (my $i = 0; $i < $size; $i++) {
        $self->{weight}[$i] += $data->[$i];
    }
}

sub _product {
    my ($vec1, $vec2) = @_;
    return 0 if !$vec1 || !$vec2;
    my $size = scalar @{ $vec1 };
    die 'illegal input vector' if scalar(@{ $vec2 }) != $size;

    my $prod = 0;
    for (my $i = 0; $i < $size; $i++) {
        $prod += $vec1->[$i] * $vec2->[$i];
    }
    return $prod;
}

sub _sign {
    my $x = shift;
    if ($x > 0) {
        return 1;
    }
    elsif ($x == 0) {
        return 0;
    }
    else {
        return -1;
    }
}

1;

# test code
package test;

use strict;
use warnings;
use Data::Dumper;

my $size = 4;
my $p = Perceptron->new($size);

# training
my @traindata = (
    {
        data => [1, 1, 0, 0],
        pn   => 1,
    },
    {
        data => [2, 1, 0, 0],
        pn   => 1,
    },
    {
        data => [0, 0, 1, 1],
        pn   => -1,
    },
    {
        data => [0, 0, 1, 2],
        pn   => -1,
    },
);
$p->train(\@traindata, 100);
print Dumper($p->{weight});

# predict
my @testdata = (
    [2, 2, 0, 0],  # maybe 1
    [1, 2, 0, 0],  # maybe 1
    [0, 0, 2, 2],  # maybe 0
    [0, 0, 2, 1],  # maybe 0
);
foreach my $data (@testdata) {
    my $result = $p->predict($data);
    print "$result\n";
}
